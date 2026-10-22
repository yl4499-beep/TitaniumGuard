# Verified course deployment

Public application: https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/

## Target and publishing path

- Owner: Yunkuan Liu (`yl4499`), Publisher role.
- Content title: TitaniumGuard.
- Content GUID: `4e02952e-c744-4f24-8791-463876e0bcb5`; content ID 534.
- Initial deployment: October 21, 2026, 19:59 Eastern (23:59 UTC).
- Initial source: `yl4499-beep/TitaniumGuard`, `main`, directory `app`, commit `aca87f7c7b39e9e664f81e7e10df72c39ebde5a8`.
- Initial bundle: 6811. Connect reported the environment build completed and launched the FastAPI application.
- Runtime: Python 3.12.4, compatible with the committed manifest's `~=3.12.0` requirement.
- Access: **Anyone - no login required**. Only synthetic datasets are bundled.

The application was created through **Publish → Import from Git** on course Posit Connect. Native Git-backed publishing reads the committed manifest. No API key was created, copied or put in a GitHub secret. GitHub contains the source and verification history; Connect performs the deployment.

The older API-key publisher workflow is retained as a **manual alternative only**, not triggered by pushes. It must not be run against the live project without deliberately reviewing the destination and migration; its original name-based configuration can create a separate content item.

## Executed checks

The browser loaded all three scenarios and displayed the expected baseline Cpl and signal counts. Independent HTTP requests without cookies or an Authorization header verified the public homepage, `/health`, API documentation, OpenAPI, all three CSV downloads, all three **complete JSON outputs** against the reviewed fixtures, and invalid-input handling.

| Dataset | Status | Baseline Cpl | Signaled builds | Monitoring nonconforming |
|---|---|---:|---:|---:|
| stable_capable | meets_target | 2.246761300154673 | 0 | 0/75 |
| mean_shift | process_shift | 2.246761300154673 | 15 | 52/75 |
| stable_incapable | below_target | 0.41803648403455207 | 0 | 10/75 |

GitHub source commit `c3166694bbf6d2020674434e1656d1b06970a036` adds repeatable public checks. Both runs succeeded:

- [Statistical/API/release checks, run 39697302948](https://github.com/yl4499-beep/TitaniumGuard/actions/runs/39697302948): `109 passed, 1 warning`; 20 manifest checksums and three dataset mirrors passed.
- [Public live verification, run 39697302954](https://github.com/yl4499-beep/TitaniumGuard/actions/runs/39697302954): all steps passed.

Actual public verification output:

```text
PASS anonymous home, health 1.0.0, API docs and OpenAPI
PASS stable_capable: full JSON and CSV match; status=meets_target; signals=0
PASS mean_shift: full JSON and CSV match; status=process_shift; signals=15
PASS stable_incapable: full JSON and CSV match; status=below_target; signals=0
PASS invalid input: HTTP 422
VERIFIED public TitaniumGuard deployment
```

To repeat the same check from the repository root:

```bash
python .github/scripts/verify-live.py https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/
```

The workflow checks a running deployment; it does not publish, create credentials, or claim that a successful CI job itself means deployment succeeded. The earlier missing-secrets deployment failure remains visible as historical evidence. The native Git deployment and public verification above are the current delivery path.

## Remaining submission work

Devpost and Canvas have **not** been submitted. Yunkuan Liu is the sole human participant. Individual-entry eligibility and truthful personal-review details remain to be confirmed. He must complete the actual Devpost form, and submit the repository URL plus the resulting Devpost project link on Canvas as directed by [kickoff slide 10](https://timothyfraser.com/sigma/slides/40_slides_recitation_8.html#10). Check the actual Canvas assignment for its deadline and required fields.
