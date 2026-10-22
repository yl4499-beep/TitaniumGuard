# Devpost submission draft — TitaniumGuard
Submission copy for Yunkuan Liu. GitHub and live application links are verified below. Personal review and individual-entry eligibility remain pending; complete them before final submission. This draft does not claim that either Devpost or Canvas has been submitted.

## Project name
TitaniumGuard

## Project owner and participants
- Project owner: **Yunkuan Liu**.
- Sole human participant: **Yunkuan Liu**.
- AI assistance: ChatGPT/Codex; it is not a team member.
- Project name: TitaniumGuard. No separate registered team name is claimed.

The event currently lists teams of 2–5. An organizer-approved individual-entry exception has not been verified. See [ownership and review status](OWNER_REVIEW.md).

## Elevator pitch
A practical strength-monitoring workbench for titanium additive manufacturing: log test coupons, detect process shifts, and separate statistical stability from capability.

## Inspiration
A contractor can pass many individual tests and still have an unreliable process. The DL aerospace-printing prompt asks for usable measurements as well as analysis. The project focuses on a quality engineer who needs to know whether a new build calls for investigation and whether an established process has enough margin above its strength requirement.

## What it does
TitaniumGuard accepts a simple CSV of build IDs, timestamps, coupon IDs and tensile strengths. Operators can also record a complete build in the interface. Optional oxygen readings, laser-power and scan-speed setpoints, powder lots and treatment IDs retain investigation context without requiring telemetry.

The app constructs X-bar and R charts using a frozen reference period. It displays one-sided Cpl for minimum-strength requirements, or Cp/Cpk only when the customer really supplies both bounds. It keeps overall-SD performance indices separate from within-build capability indices. A process alert suppresses any current capability endorsement. The user can inspect build-level reasons and download the data and analysis. The Oxygen & build strength scatter plot relates each build's recorded oxygen reading to its mean coupon strength, with signal builds highlighted. It provides descriptive investigation context, not a causal model or a predictor of finished-part strength.

## How it was built
A Python FastAPI service calls plain, framework-independent statistical functions. A lightweight browser interface renders the returned numbers; there is no separate frontend build or third-party chart CDN. The project adapts the official FastAPI starter and includes the course's local-run, manifest and deploy script structure.

## Demonstration
Three explicitly synthetic, reproducible datasets illustrate a stable process with a large strength margin, a planted mean shift beginning at build 26, and a stable process with insufficient strength margin. Each dataset has 40 builds with 5 distinct coupons per build. The sample LSL = 900 MPa and target = 1.33 are teaching inputs, not aerospace standards. See demo/README.md for measured outputs.

## Challenges
The main statistical challenge was preventing an abnormal monitoring period from contaminating its own control limits. Another was avoiding a misleading two-sided capability index when only a minimum strength matters. On the data side, the app rejects incomplete subgroups and duplicated coupon records instead of silently changing the study.

## Lessons from the project
Stability and capability answer different questions. No observed rejection in a small sample proves neither long-term conformity nor suitability for flight. Environmental context helps structure an investigation, but an association between oxygen and a shift does not establish a cause.

## What is next
Validate measurement quality, the sampling plan, and coupon-to-bracket representativeness with the contractor. Add documented investigation and corrective-action records, then evaluate a new baseline after a verified improvement. A production version would require access control, audit history and qualified release procedures.

## Built with
Python, FastAPI, JavaScript, HTML, CSS, pytest; deployed on course Posit Connect through its native Git integration.

## AI assistance
Yunkuan Liu is the sole human project owner. ChatGPT/Codex assisted with design, code, synthetic datasets, tests and documentation, as encouraged by the event. Sources, automated checks and AI-assisted numerical cross-checks are recorded in the repository. These checks are not presented as Yunkuan Liu’s personal review. His review of the code, methods and demonstration outputs remains pending; only work actually reviewed should be described as personally checked.

## Links to enter
- Actual public GitHub repository: https://github.com/yl4499-beep/TitaniumGuard
- Actual live Posit Connect application: https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/
- Demonstration video: a 2 min 29 sec preview with Chinese captions and no audio has been produced from the actual application running locally. It is included in the complete export bundle. No public video-hosting URL or Devpost upload is claimed; see [preview details](DEMO_PREVIEW.md).

## Submission status and Canvas follow-up
This file is a draft; no Devpost submission has been completed. After submitting on Devpost, the official kickoff slide 10 also asks for the repository URL and Devpost project link on Canvas. Check the course assignment for its deadline and fields.
