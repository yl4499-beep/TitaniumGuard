# Build plan
- H-01: SPEC.md; known-answer arithmetic and scope fixed. Team/repo/live URL intentionally pending.
- H-02: data/; 3 seeded CSVs + codebook; verify 40 x5, timestamps and planted shift at26.
- H-03: app/qc.py, tests/, requirements; hand fixture and degenerate inputs; independent stats review.
- H-04: app/; official FastAPI starter + same-origin dashboard; API matches core, upload/log/export usable.
- H-05: demo/; exact results and walkthrough for all3 datasets; browser interaction checks.
- H-06: deployment scripts, committed manifest and optional official CI; actual deploy requires course credentials.
- H-07: README and docs/; English presentation, submission copy, Chinese explanation, sources and honest status.
- H-08: gitignore; complete source archive; public GitHub and actual Devpost entry require user's account.

## Formulas
Xbar_i=sum(x_ij)/n; R_i=max(x_ij)-min(x_ij).
mu0=mean(Xbar_baseline); Rbar=mean(R_baseline); sigma_within=Rbar/d2.
Xbar limits=mu0 +/- A2*Rbar; R limits=D3*Rbar,D4*Rbar.
Cpl=(mu0-LSL)/(3*sigma); optional Cpu=(USL-mu0)/(3*sigma), Cp=(USL-LSL)/(6*sigma), Cpk=min(Cpl,Cpu).
P indices substitute baseline sample SD (ddof1) for sigma. Observed rejection=count outside specs / count measured.
QQ normal scores=NormalDist.inv_cdf((i-.5)/N), paired with sorted baseline observations.
Control signals: one beyond 3sigma; Xbar8 on same side, alert at eighth. No retrospective deletion.

## Decisions
User asked for full project and prioritizes easiest robust score. Choose official DL 3D Printing prompt.
Product name TitaniumGuard; do not invent registered team name.
Python for analysis; no telemetry, cloud database or frontend build required.
One-sided strength limit default; invented demo LSL900 and target1.33, not engineering specifications.
Baseline25 builds; 40 builds per demo, size5. Optional covariates logged at build level.
Use descriptive covariate display only. No causal/predictive claims.
Use independent stats-reviewer after implementation as the official workflow requests.
