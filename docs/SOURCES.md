# Sources and attribution
Accessed 2026-10-20 UTC. Sources ground requirements and formulas; all example observations and settings are invented.

1. Cornell Six Sigma Hackathon, Devpost: https://six-sigma-hackathon.devpost.com/ . Official DL Industrial Systems prompt, "3D Printing for Aerospace", and grading requirements. The page also lists Blood Banks and Civil Liberties. Prompt is summarized, not copied in full.
2. Official project repository: https://github.com/timothyfraser/sixsigmahackathon . Starter snapshot 6c702e6 (2026-10-17). FastAPI four-script starter adapted; official agent instructions retained. Project implementation and UI are new.
3. Evaluation criteria: https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/criteria.md . Working tool 25; valid analysis 25; scope 5; use case 5; minimal inputs 5; demo 10; documentation 10; datasets 5; codebook 5; public reproducibility 5.
4. Schedule: https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/schedule.md . DL submission listed as Oct 23, 2026, 3 PM Eastern. The Devpost page's event-status banner and written schedule may disagree; verify that the DL submission form is open with the organizer. Do not interpret the banner as an extension or a cancellation.
5. NIST/SEMATECH e-Handbook 6.3.2.1, Shewhart X-bar and R and S Control Charts: https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc321.htm . Xbar/R formulas and rounded A2, D3, D4 factors. This implementation consistently uses the NIST table (n = 5: D4 = 2.115).
6. NIST/SEMATECH e-Handbook 6.1.6, What is Process Capability?: https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm . Capability formulas, one-sided Cpl/Cpu and normality assumptions. The project explicitly uses within-subgroup Rbar/d2 for C indices and overall sample SD for P indices, following the official course-agent convention.
7. Course materials: https://timothyfraser.com/sigma/ . See official repository's stats-first-steering skill for baseline, subgroup and estimator conventions.
8. FastAPI documentation: https://fastapi.tiangolo.com/tutorial/first-steps/ . API framework and ASGI serving.
9. Posit Connect publishing documentation: https://docs.posit.co/connect/user/publishing-cli-apps/ and https://docs.posit.co/rsconnect-python/ . Intended course deployment route.

## AI use disclosure
OpenAI ChatGPT/Codex assisted with project design, synthetic data generation, Python implementation, tests, interface and documentation. The statistics were checked against independently computed known answers and boundary cases; verification results are recorded in demo/. The participant must review the code and be able to explain the methods. No claim is made that simulated data are field observations or that the prototype is an aerospace certification system.

## No claimed engineering authority
900 MPa (demo LSL), 1.33 (demo target), process settings and scenario shifts are invented teaching choices. No technical standard is cited as their origin. A real study requires client-approved specifications, qualified testing and a validated sampling plan.

## Expanded audit, 2026-10-20
The official README, criteria and schedule were checked again. They require a public reproducible repository and a live prototype/demo; no minimum commit count was found in the reviewed public requirements. Local checks are separate from actual GitHub Actions or course-server publishing.

Swagger UI 5.17.14 is redistributed as unmodified npm distribution assets under Apache-2.0; its LICENSE, NOTICE and exact asset hashes are included in app/static/vendor/. This makes interactive API documentation usable without an external CDN.
