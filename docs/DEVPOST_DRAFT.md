# Devpost project description — TitaniumGuard

Copy the relevant sections into the matching Devpost fields. This file contains project copy, not a submission receipt. Upload the English-captioned demo to YouTube and enter its actual viewing URL in the video field. Account actions and eligibility are tracked in [ownership and submission status](OWNER_REVIEW.md).

## Project name
TitaniumGuard

## Elevator pitch
Monitor titanium printing quality with frozen control charts, strength capability analysis, and build records.

## Project owner
Yunkuan Liu — sole human participant.

## Inspiration
The DL challenge describes an aerospace contractor whose printed titanium brackets fail strength tests. I focused on a practical question for a quality engineer: is the printing process changing, or is it consistent but too close to the minimum strength requirement? TitaniumGuard uses tensile-test coupons as a measure of process strength and keeps build conditions alongside the results for investigation.

## What it does
TitaniumGuard is a web dashboard with a Python analysis API. Users can upload a CSV or log a complete build in the interface. The four required CSV columns are build ID, build time, specimen ID and strength in MPa. Optional fields include chamber oxygen, laser power, scan speed, powder lot, machine and heat treatment.

The app estimates X-bar and R control limits from a reference period and keeps those limits fixed when checking later builds. It reports Cpl when only a minimum strength is specified, and Cp/Cpk when both specification limits are supplied. Overall-SD performance indices are reported separately. If the charts detect a process signal, a high historical baseline index does not endorse the current process.

Users can inspect flagged builds, compare oxygen readings with build mean strength, and export CSV data and JSON analysis. The environmental plot provides descriptive clues for investigation; it does not establish a cause or predict finished-part strength. Records remain in the current browser tab until exported.

## How it was built
The project adapts the official FastAPI starter. Statistical functions in Python calculate the results, and a lightweight HTML/CSS/JavaScript interface displays them. The application is deployed on the course Posit Connect server through its Git integration.

ChatGPT/Codex assisted with design, implementation, synthetic data, tests and documentation. I have personally reviewed the project. The repository includes the data generator, a codebook, known-answer checks, boundary-case tests and source references.

## Challenges
A key challenge was keeping an abnormal monitoring period from changing its own control limits. Another was using the correct one-sided capability index for a minimum-strength requirement. Input validation also matters: incomplete subgroups, duplicate specimen IDs and invalid settings produce errors instead of silently changing the study.

## Accomplishments
The working prototype demonstrates three distinct outcomes using reproducible synthetic datasets: a stable process with a large strength margin, a mean shift beginning at build 26, and a stable process with insufficient margin. The verified test suite contains 109 tests: 71 numerical/schema tests and 38 API tests. The public application has also been checked against the recorded demonstration outputs.

## What I learned
The project highlights why stability and capability need to be considered separately. A process can have no control-chart signals and still have too little strength margin. Conversely, a high historical capability index cannot describe a process after a shift. The oxygen plot also illustrates why associated changes are a starting point for investigation rather than proof of causation.

## Demonstration
Each synthetic dataset contains 40 builds with 5 distinct coupons per build. The first 25 builds form the baseline. The example minimum of 900 MPa and target of 1.33 are teaching settings, not aerospace standards.

- Stable process: baseline Cpl approximately 2.247; no flagged builds.
- Mean shift: 15 flagged builds beginning at build 26; the historical baseline Cpl remains approximately 2.247.
- Low margin: baseline Cpl approximately 0.418; no flagged builds.

The 2 min 29 sec demo is a recording of the actual application running locally, with English captions and no audio. It shows the three scenarios, CSV import, complete-build entry, and CSV/JSON exports. Exact results are documented in [the walkthrough](../demo/README.md).

## What is next
The next step is to validate measurement quality, the sampling plan and coupon-to-bracket representativeness with a contractor. Further development could add investigation records, corrective-action tracking and persistent storage. This educational prototype supports process investigation; it does not authorize part release or certify airworthiness.

## Built with
Python, FastAPI, JavaScript, HTML, CSS, pytest, Posit Connect, GitHub.

## Links
- Public repository: https://github.com/yl4499-beep/TitaniumGuard
- Live application: https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/

Video upload instructions: [DEMO_PREVIEW.md](DEMO_PREVIEW.md). Enter the actual YouTube viewing URL in Devpost; the local MP4 filename is not a submission link.
