"""Run all supplied fixtures and write exact JSON and readable result summary."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from app.qc import analyze_records,parse_csv

def main():
    outputs={}
    for name in ['stable_capable','mean_shift','stable_incapable']:
        result=analyze_records(parse_csv((ROOT/'data'/(name+'.csv')).read_text()))
        outputs[name]=result
        (ROOT/'demo'/(name+'.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(f"{name}: status={result['status']}, baseline Cpl={result['baseline']['index_value']:.6f}, signals={result['signals']['total']}, monitoring nonconforming={result['observed']['monitoring']['nonconforming']}/{result['observed']['monitoring']['n']}")
    (ROOT/'demo'/'all_results.json').write_text(json.dumps(outputs,indent=2,allow_nan=False)+'\n')
    lines=['# Demonstration — exact computed results','','Run from the project root: `python demo/run_demo.py`. These results use the supplied synthetic fixtures, baseline = 25, LSL = 900 MPa, no USL and target = 1.33. All example values and study settings are invented.','','| Dataset | Status | Baseline Cpl | Baseline Ppl | Flagged builds | Monitoring nonconforming |','|---|---|---:|---:|---:|---:|']
    for k,a in outputs.items():
        lines.append(f"| {k}.csv | {a['status']} | {a['baseline']['index_value']:.6f} | {a['baseline']['performance']['Ppl']:.6f} | {a['signals']['total']} | {a['observed']['monitoring']['nonconforming']}/{a['observed']['monitoring']['n']} |")
    a=outputs['stable_capable']
    lines+=['','## Demo preview', 'A 2 min 29 sec Chinese-captioned, silent recording of the actual local application is included in the complete export bundle. See [preview details](../docs/DEMO_PREVIEW.md) and the [English speaking script](../docs/PITCH.md). A video-hosting URL and Devpost upload remain pending.', '', '## Frozen reference limits',f"Both stable_capable and mean_shift share the identical baseline. Mean={a['baseline']['mean']:.6f} MPa; R-bar={a['baseline']['rbar']:.6f} MPa; within sigma={a['baseline']['sigma_within']:.6f} MPa; overall SD={a['baseline']['sd_overall']:.6f} MPa.",f"X-bar LCL={a['limits']['xbar']['lcl']:.6f}, UCL={a['limits']['xbar']['ucl']:.6f} MPa. R LCL={a['limits']['range']['lcl']:.6f}, UCL={a['limits']['range']['ucl']:.6f} MPa.",'','## Browser walkthrough','1. Start `bash app/testme.sh`; open the printed local URL. Load **Stable process**. Inspect R then X-bar, historical baseline Cpl and observed nonconformance. No detected signal is not proof of normality or adequacy of the measurement plan.','2. Load **Mean shift**. Verify B026 is the first flagged build, B026–B040 are flagged, and limits remain identical. The historical Cpl remains high; the current process status correctly calls for investigation. Scroll below the control charts to **Oxygen & build strength**. The scatter plot maps oxygen (ppm) to build mean strength (MPa); 40 points represent 40 builds and the 15 signal builds are red. Say “association, not a proven cause.”','3. Load **Low margin**. The study is not signaling a change, but Cpl is below 1.33. This separates predictable variation from adequate strength margin.','4. Upload one CSV from data/ to reproduce the same output. Try an invalid file: it should give a specific validation error, not partial results.','5. Log a complete new build with the same subgroup size and later timestamp, then download the updated CSV. Only browser-session memory holds edits until exported.','6. Download the JSON report, inspect the method notes and open `/docs` for the API interface.','', '## Interpretation limits','These are selected synthetic demonstration fixtures. The codebook discloses seed selection. The tool does not predict part failures or certify airworthiness. A new baseline after a verified corrective action is a new study, not a way to hide an existing signal.','', '## Verification','Statistical unit tests: `python -m pytest tests -q`. API integration checks: `python -m pytest tests app/test_api.py -q`. Known-answer arithmetic and independent review are recorded in `STATISTICS_REVIEW.md`. Actual deployment and public Devpost submission remain separate checks.']
    (ROOT/'demo'/'README.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
