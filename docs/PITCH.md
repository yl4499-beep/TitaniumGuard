# Three-minute demonstration script

Speaker: **Yunkuan Liu**. This is a rehearsal script, not evidence of a completed personal review or submitted recording. The timing is a target; practise with the app before recording.

**0:00–0:25 — Problem and user**
“I’m Yunkuan Liu, the project owner. With ChatGPT/Codex assistance, I built TitaniumGuard, for the DL 3D Printing for Aerospace challenge. It helps a quality engineer understand whether a titanium printing process is changing and whether it has enough margin over a client’s strength requirement. The data in this demonstration are synthetic.”

**0:25–0:55 — Collection and baseline**
“Each row is one destructive tensile test on a distinct coupon. Five coupons from the same qualified build form a subgroup. The operator records IDs, time and strength; oxygen and recipe fields are optional context. The app estimates control limits from the first 25 builds, then freezes them for later builds. The 900 MPa minimum and 1.33 target are demonstration inputs.”

**0:55–1:25 — Stable case**
Load Stable process. Show the R chart first, then X-bar. “The range chart monitors variation within builds; the mean chart monitors movement between builds. The app uses R-bar divided by d2 for within-process sigma. There is only a minimum strength in this example, so the relevant index is Cpl. This is an estimated baseline index, conditional on the sampling and distribution assumptions.”

**1:25–1:55 — Shift case**
Load Mean shift. “The planted shift starts at build 26. Notice that the limits have not widened. The current process triggers investigation even though its historical baseline had a high capability index. Scroll below the control charts to Oxygen & build strength. Each point represents a build: recorded oxygen is on the x-axis and average coupon strength is on the y-axis. The two synthetic clusters show the planted association, with signal builds in red. That is a clue to investigate, not proof of causation.”

**1:55–2:20 — Stable but inadequate**
Load Low margin. “This illustrates why a stable chart does not imply adequate capability. The output can remain statistically consistent while lying too close to the lower specification. The quality engineer needs a verified process improvement, rather than treating every ordinary fluctuation as a special cause.”

**2:20–2:45 — Working tool**
Show CSV upload, Log a build, exported JSON and CSV, plus the method panel. “Invalid or incomplete subgroups produce a clear error. The calculations run in Python and are checked against hand-worked values and deliberately planted anomalies. Documentation includes a codebook and reproducible generator.”

**2:45–3:00 — Limits and next step**
“This prototype supports process investigation; it does not release individual brackets or certify aircraft parts. The next step would be validating the measurement system and the coupon sampling plan with a contractor.”

## Questions to practise
- Why not use overall standard deviation for Cpl? Within-subgroup variation and between-build changes describe different aspects; the app labels overall-SD indices as P indices.
- Are control limits specifications? No. Control limits summarize reference-process variation; specifications come from engineering requirements.
- Why Cpl rather than Cp? A minimum strength is a one-sided requirement. Cp requires an actual upper limit too.
- Why not recalculate limits after the shift? That can normalize the problem; investigate first and establish a new justified baseline after corrective action.
- Does oxygen cause the shift? These are synthetic associated changes. A real causal claim needs a designed study and process knowledge.
- Can the app approve a part for flight? No. Destructive test coupons are process proxies; qualified part-release procedures remain separate.
