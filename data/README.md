# Dataset codebook and collection plan
All values are **synthetic**. No company, patient, aircraft or real production data are used. The 900 MPa minimum and 1.33 study target are demonstration assumptions, not ASTM, customer or aviation requirements. A real user must supply approved engineering requirements.

## Files
Each CSV contains 200 coupon results from 40 chronological builds, 5 coupons per build. Use the first 25 builds as the frozen baseline. Run `python data/generate.py` from the project root to recreate all three using the fixed seed42. Python's standard `random.Random` Gaussian generator is used; Seed42 was selected to illustrate the intended three states without an unrelated random control-chart signal. An earlier trial seed produced an incidental range alert; it was not used for these teaching fixtures. These are selected synthetic demonstrations, not unbiased Monte Carlo estimates of alarm performance. No rows from real production have been removed. Pin Python3.12 for identical reproduction.
- `stable_capable.csv`: independent normal strengths, mean1000 MPa and SD15 MPa for all40 builds.
- `mean_shift.csv`: the same seeded scenario, but the strength mean falls from1000 to890 MPa from build26; SD remains15. The simulated oxygen mean simultaneously increases from65 to260 ppm. This is a deliberately planted association, not an empirical causal relationship.
- `stable_incapable.csv`: independent normal strengths, mean925 MPa and SD22 MPa throughout. The process can be stable while having too little margin over900.
- `generate.py`: standalone deterministic generator. Metadata draws consume the same random stream in each scenario; seeds and distributions are fully visible.

## Variables
| Column | Type / units | Definition and practical source |
|---|---|---|
| build_id | text | Unique production-build identifier from the job traveler. One build is one subgroup. |
| build_time | ISO8601 timestamp | Build start time; one identical value per build. Use a consistent timezone in actual collection. |
| specimen_id | text | Unique coupon ID tied to build, orientation and location through a traveler. Never repeat a tensile measurement on one destroyed coupon. |
| strength_mpa | number, MPa | Ultimate tensile strength (maximum force / original cross-sectional area), recorded from a calibrated tensile-test system. Positive, finite values required. |
| machine_id | text | Printer asset ID. Analyze one qualified route and machine at a time. |
| powder_lot | text | Feedstock lot from supplier and powder-reuse records. Do not mix materially different populations. |
| oxygen_ppm | number, ppm | Build-level chamber oxygen reading, consistently defined as the recorded maximum during the build. Read display/log or a calibrated meter. Synthetic values do not define acceptable process windows. |
| laser_power_w | number, W | Recorded laser-power setpoint on the job traveler; it is not an in-situ measurement of delivered energy. |
| scan_speed_mm_s | number, mm/s | Recorded scan-speed setpoint from the same parameter recipe. |
| heat_treatment | text | Treatment route ID. Keep route, build orientation, geometry and alloy consistent in a study. |
| notes | text | Operator observations and relevant maintenance/context. No personal details needed. |

The four required columns are build_id, build_time, specimen_id and strength_mpa. Use the exact documented column names: extra/unknown columns (including misspellings or trailing spaces) are rejected rather than silently discarded. In JSON records, identifiers, timestamps and text metadata must be strings; numeric IDs should be quoted. UTF-8 CSV supports LF, CRLF and CR line endings. Context columns are optional, but if supplied they must be consistent within each build. No undocumented imputation or silent row deletion occurs. All identifiers must be unique in their intended scope; timestamps strictly increase between builds.

## Real collection protocol
1. Define one CTQ: coupon ultimate tensile strength for one qualified bracket printing route. Obtain the customer minimum, any actual maximum, and study target separately from measurements. Do not estimate specification limits from data.
2. Agree with the testing engineer on five distinct representative coupons per build, standardized orientation/location allocation and specimen preparation. Record coupon geometry, alloy, test method, heat-treatment recipe and calibration in a study record. The app's basic CSV is not a complete aerospace traceability system.
3. During printing, record oxygen, job recipe, powder lot, machine and time using readings available to technicians. These are proposed manual logging fields; the prompt assumes no telemetry exists.
4. Destructively test each coupon once after the specified post-processing. Record MPa to the instrument's validated resolution. Repeated readouts of the same coupon are not independent samples.
5. Gather a representative baseline of at least25 builds (125 results for n5). Review range then mean charts, measurement adequacy, normality and serial dependence. Investigate special causes; any excluded build must have an engineering justification and a separate audit record. This prototype never silently removes data.
6. Freeze the baseline, add later builds, and investigate control signals and nonconforming coupons. Coupon evidence supports process review, not an individual part-release or airworthiness decision. Validate coupon-to-bracket relevance separately.
7. After a documented corrective action, collect a new baseline in a separate study; do not continually widen limits by including excursions.
