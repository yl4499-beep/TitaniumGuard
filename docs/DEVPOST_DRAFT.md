# Devpost submission draft — TitaniumGuard
Use after reading the code and running the demonstrations. Add the actual team, public GitHub URL and live course Posit Connect URL before submission. Do not submit placeholders.

## Project name
TitaniumGuard

## Elevator pitch
A practical strength-monitoring workbench for titanium additive manufacturing: log test coupons, detect process shifts, and separate statistical stability from capability.

## Inspiration
A contractor can pass many individual tests and still have an unreliable process. The DL aerospace-printing prompt asks for usable measurements as well as analysis. We focused on a quality engineer who needs to know whether a new build calls for investigation and whether an established process has enough margin above its strength requirement.

## What it does
TitaniumGuard accepts a simple CSV of build IDs, timestamps, coupon IDs and tensile strengths. Operators can also record a complete build in the interface. Optional oxygen readings, laser-power and scan-speed setpoints, powder lots and treatment IDs retain investigation context without requiring telemetry.

The app constructs X-bar and R charts using a frozen reference period. It displays one-sided Cpl for minimum-strength requirements, or Cp/Cpk only when the customer really supplies both bounds. It keeps overall-SD performance indices separate from within-build capability indices. A process alert suppresses any current capability endorsement. The user can inspect build-level reasons and download the data and analysis.

## How it was built
A Python FastAPI service calls plain, framework-independent statistical functions. A lightweight browser interface renders the returned numbers; there is no separate frontend build or third-party chart CDN. The project adapts the official FastAPI starter and includes the course's local-run, manifest and deploy script structure.

## Demonstration
Three explicitly synthetic, reproducible datasets illustrate a stable process with a large strength margin, a planted mean shift beginning at build26, and a stable process with insufficient strength margin. Each dataset has40 builds with5 distinct coupons per build. The sample LSL900 MPa and target1.33 are teaching inputs, not aerospace standards. See demo/README.md for measured outputs.

## Challenges
The main statistical challenge was preventing an abnormal monitoring period from contaminating its own control limits. Another was avoiding a misleading two-sided capability index when only a minimum strength matters. On the data side, we reject incomplete subgroups and duplicated coupon records instead of silently changing the study.

## What we learned
Stability and capability answer different questions. No observed rejection in a small sample proves neither long-term conformity nor suitability for flight. Environmental context helps structure an investigation, but an association between oxygen and a shift does not establish a cause.

## What is next
Validate measurement quality, the sampling plan, and coupon-to-bracket representativeness with the contractor. Add documented investigation and corrective-action records, then evaluate a new baseline after a verified improvement. A production version would require access control, audit history and qualified release procedures.

## Built with
Python, FastAPI, JavaScript, HTML, CSS, pytest; intended deployment on course Posit Connect.

## AI assistance
ChatGPT/Codex assisted with design, code, synthetic datasets, tests and documentation, as encouraged by the event. Sources and executed verification are included. The team reviewed [replace this bracketed statement with the review actually performed].

## Links to enter
- Actual public GitHub repository: https://github.com/yl4499-beep/TitaniumGuard
- Actual live Posit Connect application: pending deployment and public-access verification.
- Demonstration video: record the provided walkthrough if the submission form requests a video; no recording has been fabricated.
