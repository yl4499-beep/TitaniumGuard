# TitaniumGuard app
FastAPI serves one HTML/CSS/JavaScript dashboard and a Python analysis API from the same origin. It adapts the official Six Sigma FastAPI starter, with new framework-free calculations in qc.py.

## Run
From the project root: `bash app/testme.sh`. The script bootstraps `.venv` and prints the local address. The same command works from another directory using the script's absolute path. Python 3.12 is the tested interpreter.

To use an existing environment: `TITANIUM_PYTHON=/absolute/path/to/python PORT=8765 bash app/testme.sh`. That environment must already contain requirements.txt. For external hosting, use `python -m uvicorn server:api --host 0.0.0.0 --port 8000` from this app directory, with an appropriate hosting/security configuration.

## API
GET /health -> status ok.
GET /api/datasets -> three synthetic fixture names.
GET /api/datasets/stable_capable -> CSV (other names: mean_shift, stable_incapable).
POST /api/analyze -> analysis JSON; GET /docs -> OpenAPI UI.

Example request shape:
```json
{"csv_text":"build_id,build_time,specimen_id,strength_mpa\n...","lsl":900,"usl":null,"baseline_builds":25,"target":1.33}
```
The ellipsis is explanatory, not runnable data. A runnable request using the actual supplied fixture, from the project root:
```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import json, urllib.request
payload={'csv_text':Path('data/stable_capable.csv').read_text(),'lsl':900,'baseline_builds':25,'target':1.33}
request=urllib.request.Request('http://127.0.0.1:8000/api/analyze',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(request) as response:
    result=json.load(response)
print(result['status'],result['baseline']['capability']['Cpl'])
PY
```
Expected: `meets_target 2.246761300154673` (minor final floating-point digits may vary).

The alternative records input is a list of objects with the documented CSV fields. Supply records or csv_text, never both. Unsupported units must be converted before upload. No missing strength imputation, row deletion, subgroup completion or automatic reordering is performed. The documented body limit and row limit keep this prototype small.

## Responses and parameters
- lsl: positive client minimum in MPa; default 900 is demonstration-only.
- usl: optional finite value greater than lsl. Omit for a one-sided requirement.
- baseline_builds: integer 2 or more, no larger than supplied builds. Under 25 yields preliminary interpretation.
- target: positive study target for Cpl or Cpk; default 1.33 is illustrative.
- metadata: counts, settings, subgroup size, constants, units and rules.
- baseline: mean, R-bar, within sigma, sample SD, C and P dictionaries, historical index, baseline signals.
- limits: xbar and range, each with lcl,cl,ucl.
- groups: one chronological entry per build, including measurements, recorded context, signals and observed counts.
- status: baseline_unstable, process_shift, preliminary, below_target or meets_target.
- observed: baseline,monitoring,all counts/fractions; empty monitoring fraction is null.
- qq: normal scores and sorted baseline values for visual distribution review.
- warnings/recommendation: explain conditional interpretation and next investigation step.

The Cpl reported during a process_shift is explicitly a historical baseline value; it is not a recalculated estimate of the shifted process.

## Four-script contract
`testme.sh` starts locally; `manifestme.sh` creates a real Posit manifest; `deployme.sh` publishes using the account credentials supplied through the local environment; this README documents inputs and outputs. `server:api` is the explicit ASGI entrypoint.

Application requirements are pinned. Development/test dependencies are separate. Package-generated caches and environments are excluded from the release archive. Rebuild manifest.json after changing source files or requirements.

## State and scope
The browser holds logged builds until export; the server does not persist uploaded data. There is no user account system, audit history or live sensor feed. All demonstration datasets are synthetic and are bundled under sample_data/. Source datasets under ../data/ are authoritative.

## Audit hardening
Request option names are strict: unknown fields are rejected. LSL, USL and target accept finite positive JSON numbers, including integers, but reject booleans and numeric strings. Validation failures return HTTP 422 JSON without echoing raw submitted values. CSV/record fields must match the documented schema. `/docs` uses locally bundled Swagger UI assets and works under a reverse-proxy URL prefix. `/redoc` is not provided.
