# TitaniumGuard — project specification

## 1. Team and prompt
- Project name: TitaniumGuard (working product name, not a registered team name).
- Project owner and sole human participant: **Yunkuan Liu**, confirmed by the user on 2026-10-22.
- AI assistance: ChatGPT/Codex; not a human teammate.
- No separate registered team name has been supplied. The official event lists teams of 2–5; approval for an individual entry has not been verified. Record only actual participants in Devpost.
- Track: Virtual DL Challenge, 7 days.
- Official prompt: DL Industrial Systems — **3D Printing for Aerospace** (the website gives no number).
- Prompt source: https://six-sigma-hackathon.devpost.com/ (retrieved 2026-10-20 UTC).
- Prompt summary: a contractor prints titanium brackets that fail strength tests; define environmental and stress-related records, monitor process capability, flag issues, and support investigation.
- Public repository: https://github.com/yl4499-beep/TitaniumGuard (published 2026-10-21). Live course application: https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/ (deployed 2026-10-21 Eastern; anonymous access verified).

## 2. User and decision
A contractor's quality engineer reviews destructive tensile-test coupons from each print build. The tool distinguishes an unusual process shift from a stable process with inadequate strength margin and provides build records to investigate. Coupons are proxies for process strength, not proof of every bracket's fitness for flight.

## 3. Inputs
- CSV: `build_id`, `build_time`, `specimen_id`, `strength_mpa` required. Unknown fields are rejected; IDs/timestamps/text metadata must be strings. Standard LF/CRLF/CR line endings are supported.
- Exactly 5 independently tested coupons per build in the demos; equal subgroup sizes 2–10 supported. A subgroup represents the same machine, geometry, material, orientation, and heat-treatment route.
- Optional build fields: `machine_id`, `powder_lot`, `oxygen_ppm`, `laser_power_w`, `scan_speed_mm_s`, `heat_treatment` and `notes`. Log manually from machine displays / travelers; no telemetry required.
- User inputs: minimum acceptable strength (LSL, MPa), baseline build count, and study target index. Optional USL only if actually specified by the customer. Demo LSL=900 MPa and target=1.33 are invented teaching settings, not aerospace standards.
- Strength means coupon ultimate tensile strength from a calibrated test machine. Record test method, orientation, specimen preparation and calibration in the real collection procedure.

## 4. Statistics and known answers
Method: X-bar and R charts on chronological rational subgroups, with limits frozen from the first B builds. Review R first. Estimate within-subgroup sigma as baseline R-bar / d2, never from overall SD. Use n-specific A2/D3/D4 tables; d2 for n=2..10 is [1.128,1.693,2.059,2.326,2.534,2.704,2.847,2.970,3.078].
- X-bar limits = baseline grand mean +/- A2 * R-bar.
- R limits = D3 * R-bar and D4 * R-bar.
- Signals: one mean or range outside its 3-sigma limits; also eight consecutive X-bar means strictly on one side of the baseline center. Mark the eighth and subsequent points, do not backdate an alert. State this subset explicitly; do not claim all Western Electric rules.
- Capability uses baseline data only: Cpl=(mean-LSL)/(3*sigma_within). With an actual USL: Cpu=(USL-mean)/(3*sigma_within); Cp=(USL-LSL)/(6*sigma_within); Cpk=min(Cpl,Cpu). Without USL, Cp/Cpk/Cpu are null and use the label Cpl.
- Baseline performance Ppl/Ppu/Pp/Ppk uses the baseline sample SD (ddof=1), consistently labeled. Current monitoring rejection fraction uses raw observed coupons and the given limits; do not extrapolate defect forecasts.
- No capability endorsement if baseline or monitoring signals occur. Report historical baseline indices, with a clear warning. Fewer than 25 baseline builds is preliminary; no qualified assessment. A normal Q-Q plot of baseline values supports visual inspection, but does not prove normality. Independence, approximately normal baseline output, representative subgrouping and measurement adequacy need engineering review.
- No p-values, causal models, lifetime predictions, predicted defects or automatic release approvals.

Known-answer fixture: three size-5 groups [98,99,100,101,102], [99,100,101,102,103], [100,101,102,103,104]; LSL90, USL110, baseline3. Mean=(100+101+102)/3=101; R-bar=(4+4+4)/3=4; sigma=4/2.326=1.7196904557; Xbar LCL=101-.577*4=98.692, UCL=103.308; R LCL=0, UCL=2.115*4=8.460 (NIST rounded table constant). Cpl=11*2.326/12=2.1321666667; Cpu=Cpk=9*2.326/12=1.7445; Cp=20*2.326/24=1.9383333333. Baseline sample SD=sqrt(40/14)=1.6903085095. Ppl=11/(3*sqrt(40/14)); Ppk=9/(3*sqrt(40/14)); Pp=20/(6*sqrt(40/14)). All calculations shown despite preliminary study size.
Degenerate cases: zero within-build variation, n=1, unequal subgroup sizes, nonfinite or missing strength, repeated specimen IDs, inconsistent build metadata, timestamps not ordered, invalid limits -> clear errors; never silently drop a row or return infinity.
Planted shift: append low-strength build(s) to a stable baseline and assert the first displaced mean is signaled without changing the limits.
References: NIST/SEMATECH handbook sections 6.3.2.1 (charts) and 6.1.6 (capability); course convention for within vs overall estimators. Tabulated constants are rounded; document this.

## 5. Delivery
FastAPI Python API with a same-origin HTML/CSS/JavaScript dashboard. Start from the official `demos/fastapi` template. Statistics live in `app/qc.py`; UI displays Python results. No node build or external chart CDN required. Keep testme.sh, manifestme.sh, deployme.sh and README.md. Course Posit Connect is the intended deployment target; local functionality and deploy preparation are distinct from a verified live deployment.

## 6. Outputs
State and recommendation, sample counts, baseline Cpl (or Cp/Cpk when USL exists), baseline P indices, X-bar/R charts, Q-Q plot, chronological build table with reason flags, environmental context, observed nonconformance, downloadable JSON and CSV. Form entry adds a complete build in browser memory and allows CSV export; there is no shared persistent database.

## 7. Test datasets
Three synthetic CSVs, each 40 chronological builds x5 coupons: stable_capable.csv, mean_shift.csv (shift begins build26), stable_incapable.csv. All use reproducible seeded generation and have an explicit codebook and collection protocol. The third case is a stable process with too little margin over LSL, not an invalid input; degenerate cases live in unit tests.

## 8. Documentation and reproducibility
Root README, app README, data codebook/generator, exact demo results and walkthrough, English pitch/Devpost draft, Chinese study guide, source list, tests and Posit scripts. No invented team identity, publication URL or score. Final user account actions remain clearly pending if credentials are unavailable.

## 9. Out of scope
Flight certification; individual bracket release; forecasting; causal inference; automatic parameter tuning; mixed machine pooling; telemetry; user accounts or database. No universal titanium strength or regulatory threshold is claimed.
