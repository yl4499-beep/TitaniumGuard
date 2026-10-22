# Demonstration — exact computed results

Run from the project root: `python demo/run_demo.py`. These results use the supplied synthetic fixtures, baseline = 25, LSL = 900 MPa, no USL and target = 1.33. All example values and study settings are invented.

| Dataset | Status | Baseline Cpl | Baseline Ppl | Flagged builds | Monitoring nonconforming |
|---|---|---:|---:|---:|---:|
| stable_capable.csv | meets_target | 2.246761 | 2.444170 | 0 | 0/75 |
| mean_shift.csv | process_shift | 2.246761 | 2.444170 | 15 | 52/75 |
| stable_incapable.csv | below_target | 0.418036 | 0.454766 | 0 | 10/75 |

## Demo preview
A 2 min 29 sec English-captioned, silent recording of the actual local application is available separately as `TitaniumGuard_Demo_EN.mp4`. See [preview details](../docs/DEMO_PREVIEW.md) and the [English speaking script](../docs/PITCH.md). Video hosting and Devpost submission have not yet been verified.

## Frozen reference limits
Both stable_capable and mean_shift share the identical baseline. Mean=1001.919120 MPa; R-bar=35.171200 MPa; within sigma=15.120894 MPa; overall SD=13.899620 MPa.
X-bar LCL=981.625338, UCL=1022.212902 MPa. R LCL=0.000000, UCL=74.387088 MPa.

## Browser walkthrough
1. Start `bash app/testme.sh`; open the printed local URL. Load **Stable process**. Inspect R then X-bar, historical baseline Cpl and observed nonconformance. No detected signal is not proof of normality or adequacy of the measurement plan.
2. Load **Mean shift**. Verify B026 is the first flagged build, B026–B040 are flagged, and limits remain identical. The historical Cpl remains high; the current process status correctly calls for investigation. Scroll below the control charts to **Oxygen & build strength**. The scatter plot maps oxygen (ppm) to build mean strength (MPa); 40 points represent 40 builds and the 15 signal builds are red. Say “association, not a proven cause.”
3. Load **Low margin**. The study is not signaling a change, but Cpl is below 1.33. This separates predictable variation from adequate strength margin.
4. Upload one CSV from data/ to reproduce the same output. Try an invalid file: it should give a specific validation error, not partial results.
5. Log a complete new build with the same subgroup size and later timestamp, then download the updated CSV. Only browser-session memory holds edits until exported.
6. Download the JSON report, inspect the method notes and open `/docs` for the API interface.

## Interpretation limits
These are selected synthetic demonstration fixtures. The codebook discloses seed selection. The tool does not predict part failures or certify airworthiness. A new baseline after a verified corrective action is a new study, not a way to hide an existing signal.

## Verification
Statistical unit tests: `python -m pytest tests -q`. API integration checks: `python -m pytest tests app/test_api.py -q`. Known-answer arithmetic and a separate AI-assisted review are recorded in [STATISTICS_REVIEW.md](STATISTICS_REVIEW.md). The public deployment is documented in [DEPLOYMENT.md](../docs/DEPLOYMENT.md); final submission status is tracked separately in [OWNER_REVIEW.md](../docs/OWNER_REVIEW.md).
