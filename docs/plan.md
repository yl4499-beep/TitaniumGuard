# Build plan
- H-01: SPEC.md; known-answer arithmetic and scope fixed. Yunkuan Liu is the sole human owner; public repository and live application are verified. Personal review is confirmed; individual-entry eligibility remains unverified.
- H-02: data/; 3 seeded CSVs + codebook; verify 40 × 5, timestamps and planted shift at build 26.
- H-03: app/qc.py, tests/, requirements; hand fixture and degenerate inputs; separate AI-assisted statistical review.
- H-04: app/; official FastAPI starter + same-origin dashboard; API matches core, upload/log/export usable.
- H-05: demo/; exact results and walkthrough for all 3 datasets; browser interaction checks.
- H-06: deployment scripts, committed manifest and optional official CI; native Git deployment to course Posit Connect completed; anonymous live checks passed.
- H-07: README and docs/; optional speaking script, English submission copy, Chinese study guide, sources and accurate status.
- H-08: gitignore; complete source archive; public GitHub is available; actual Devpost and Canvas submissions have not yet been verified.

## Formulas
Xbar_i=sum(x_ij)/n; R_i=max(x_ij)-min(x_ij).
mu0=mean(Xbar_baseline); Rbar=mean(R_baseline); sigma_within=Rbar/d2.
Xbar limits=mu0 +/- A2*Rbar; R limits=D3*Rbar,D4*Rbar.
Cpl=(mu0-LSL)/(3*sigma); optional Cpu=(USL-mu0)/(3*sigma), Cp=(USL-LSL)/(6*sigma), Cpk=min(Cpl,Cpu).
P indices substitute baseline sample SD (ddof1) for sigma. Observed rejection=count outside specs / count measured.
QQ normal scores=NormalDist.inv_cdf((i-.5)/N), paired with sorted baseline observations.
Control signals: one beyond 3sigma; Xbar8 on same side, alert at eighth. No retrospective deletion.

## Decisions
The project uses the official DL 3D Printing for Aerospace prompt and a focused, testable statistical scope.
Product name TitaniumGuard; do not invent registered team name.
Python for analysis; no telemetry, cloud database or frontend build required.
One-sided strength limit default; invented demo LSL = 900 MPa and target = 1.33, not engineering specifications.
Baseline 25 builds; 40 builds per demo, size 5. Optional covariates logged at build level.
Use descriptive covariate display only. No causal/predictive claims.
A separate AI-assisted statistical review was performed after implementation. Its evidence is retained in demo/STATISTICS_REVIEW.md.

## Submission documentation update — 2026-10-22
H-10 records the owner-confirmed personal review and English-captioned recording. H-11 reconciles project descriptions, current status, historical audit notes and video upload instructions. CONTRACT.yaml is the task ledger.
