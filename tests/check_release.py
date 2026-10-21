"""Validate reproducible release files without contacting a publishing server."""
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def main():
    app = ROOT / 'app'
    manifest = json.loads((app / 'manifest.json').read_text())
    assert manifest['metadata'] == {'appmode': 'python-fastapi', 'entrypoint': 'server:api'}
    assert manifest['python']['version'] == (app / '.python-version').read_text().strip()
    for name, details in manifest['files'].items():
        relative = PurePosixPath(name)
        assert not relative.is_absolute() and '..' not in relative.parts, name
        assert not any(part.startswith('.env') or part in {'.git', '.venv', '__pycache__', '.rsconnect-python', 'rsconnect-python'} for part in relative.parts), name
        path = app / name
        assert path.is_file(), f'Missing manifest file: {name}'
        assert hashlib.md5(path.read_bytes()).hexdigest() == details['checksum'], f'Stale manifest checksum: {name}'
    datasets = list((ROOT / 'data').glob('*.csv'))
    assert len(datasets) == 3
    for path in datasets:
        assert path.read_bytes() == (app / 'sample_data' / path.name).read_bytes(), path.name
    for required in ['README.md', 'SPEC.md', 'data/README.md', 'demo/README.md', 'docs/SOURCES.md', 'docs/DEVPOST_DRAFT.md']:
        assert (ROOT / required).is_file(), required
    print(f'PASS release: {len(manifest["files"])} manifest checksums, 3 identical dataset pairs, Python version and required documentation.')


if __name__ == '__main__':
    main()
