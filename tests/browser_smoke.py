"""Real-browser acceptance checks. Run directly, not through pytest.

Install the optional browser dependencies listed in README.md first. This
starts and stops its own temporary local server; it makes no external writes.
"""
from pathlib import Path
import csv
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
passed = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    passed.append(name)
    print('PASS', name, flush=True)


def main():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    server_code = (
        'from fastapi import FastAPI; from app.server import api; import uvicorn; '
        'host=FastAPI(); host.mount("/content/titanium",api); host.mount("/",api); '
        f'uvicorn.run(host,host="127.0.0.1",port={port},log_level="warning")'
    )
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    with tempfile.TemporaryDirectory(prefix='titanium-browser-') as tmp:
        with open(Path(tmp) / 'server.log', 'w+') as log:
            proc = subprocess.Popen([sys.executable, '-c', server_code], env=env, stdout=log, stderr=log)
            try:
                base = f'http://127.0.0.1:{port}'
                for _ in range(100):
                    try:
                        if urlopen(base + '/health', timeout=1).status == 200:
                            break
                    except OSError:
                        time.sleep(.1)
                else:
                    raise RuntimeError('Local test server did not become ready')
                with sync_playwright() as pw:
                    browser = pw.chromium.launch()
                    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
                    page = context.new_page()
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.goto(base + '/')
                    page.wait_for_function('result !== null && !busy')
                    check('initial analysis and four charts', page.locator('#results svg').count() == 4)
                    for name, status, signals in [('stable_capable', 'meets_target', 0), ('mean_shift', 'process_shift', 15), ('stable_incapable', 'below_target', 0)]:
                        page.locator(f'[data-demo="{name}"]').click()
                        page.wait_for_function(f'!busy && result.status === "{status}"')
                        check('scenario ' + name, page.locator('#signal-value').inner_text() == str(signals))
                    page.locator('[data-demo="mean_shift"]').click()
                    page.wait_for_function('!busy && result.status === "process_shift"')
                    page.locator('#record-filter').select_option('flagged')
                    check('filter shows 15 flagged builds', page.locator('#build-rows tr').count() == 15)
                    page.locator('#record-filter').select_option('all')
                    with page.expect_download() as event:
                        page.locator('#export-csv').click()
                    csv_data = Path(event.value.path()).read_text()
                    check('CSV export contains 200 coupon rows', len(list(csv.DictReader(io.StringIO(csv_data)))) == 200)
                    with page.expect_download() as event:
                        page.locator('#export-json').click()
                    exported = json.loads(Path(event.value.path()).read_text())
                    check('JSON export matches displayed result', exported == page.evaluate('result'))
                    page.locator('#csv-file').set_input_files({'name': 'roundtrip.csv', 'mimeType': 'text/csv', 'buffer': csv_data.encode()})
                    page.wait_for_function('!busy && sourceLabel.includes("roundtrip.csv")')
                    check('CSV export/import round trip', page.evaluate('result.baseline') == exported['baseline'])
                    page.locator('#csv-file').set_input_files({'name': 'invalid.csv', 'mimeType': 'text/csv', 'buffer': b'wrong,headers\n1,2'})
                    page.locator('#error').wait_for(state='visible')
                    check('invalid CSV retains previous result', page.evaluate('result') == exported)
                    page.locator('#usl').fill('1100')
                    check('unapplied settings explicitly flagged', page.locator('#settings-note').is_visible() and page.locator('#export-json').is_disabled() and page.locator('#log-open').is_disabled())
                    page.locator('#reanalyze').click()
                    page.wait_for_function('!busy && result.metadata.usl === 1100')
                    check('two-sided Cpk and capability table', page.locator('#index-label').inner_text() == 'Cpk' and page.evaluate('result.baseline.capability.Cp !== null'))
                    page.locator('#usl').fill('800')
                    page.locator('#reanalyze').click()
                    page.locator('#error').wait_for(state='visible')
                    check('invalid settings retain applied result', page.evaluate('result.metadata.usl') == 1100)
                    check('invalid settings cannot label an exported result', page.locator('#export-json').is_disabled())
                    page.locator('#usl').fill('')
                    page.locator('#reanalyze').click()
                    page.wait_for_function('!busy && result.metadata.usl === null')
                    page.locator('#log-open').click()
                    page.locator('#log-id').fill('B041')
                    page.locator('#log-time').fill('2026-09-21T08:00')
                    page.locator('#log-strengths').fill('1000,1001,1002,1003,1004')
                    page.locator('#log-save').click()
                    page.wait_for_function('!busy && result.metadata.n_records === 205')
                    check('manual complete build appends five coupons', not page.locator('#log-dialog').is_visible())
                    page.locator('#log-open').click()
                    page.locator('#log-id').fill('B041')
                    page.locator('#log-time').fill('2026-09-22T08:00')
                    page.locator('#log-strengths').fill('1000,1001,1002,1003,1004')
                    page.locator('#log-save').click()
                    page.locator('#log-error').wait_for(state='visible')
                    check('duplicate build rejected without losing data', page.evaluate('result.metadata.n_records') == 205)
                    page.locator('#log-cancel').click()
                    utc_csv = (ROOT / 'data/stable_capable.csv').read_text().replace('T08:00:00', 'T08:00:00Z').replace('T20:00:00', 'T20:00:00Z')
                    page.locator('#csv-file').set_input_files({'name': 'utc.csv', 'mimeType': 'text/csv', 'buffer': utc_csv.encode()})
                    page.wait_for_function('!busy && sourceLabel.includes("utc.csv")')
                    page.locator('#log-open').click()
                    check('manual timestamp timezone explicitly shown', 'UTC (Z)' in page.locator('#log-time-note').inner_text())
                    page.locator('#log-id').fill('B041')
                    page.locator('#log-time').fill('2026-09-21T08:00')
                    page.locator('#log-strengths').fill('1000,1001,1002,1003,1004')
                    page.locator('#log-save').click()
                    page.wait_for_function('!busy && result.metadata.n_records === 205')
                    check('manual timestamp preserves declared UTC zone', page.evaluate('result.groups.at(-1).time') == '2026-09-21T08:00Z')
                    check('synthetic practice records remain identified', 'still includes synthetic' in page.locator('#source-note').inner_text())
                    for width in [390, 768, 1440]:
                        page.set_viewport_size({'width': width, 'height': 1000})
                        page.wait_for_timeout(200)
                        check(f'no horizontal page overflow at {width}px', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
                    page.goto(base + '/content/titanium/')
                    page.wait_for_function('result !== null && !busy')
                    check('reverse-proxy prefix assets and API', page.locator('#index-value').inner_text() == '2.247')
                    page.goto(base + '/content/titanium/docs')
                    page.wait_for_selector('.swagger-ui .info .title')
                    check('reverse-proxy prefix interactive API docs', page.locator('.swagger-ui .info .title').inner_text().startswith('TitaniumGuard'))
                    check('no browser JavaScript errors', not errors)
                    browser.close()
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
    print(json.dumps({'browser_checks_passed': len(passed), 'checks': passed}, indent=2))


if __name__ == '__main__':
    main()
