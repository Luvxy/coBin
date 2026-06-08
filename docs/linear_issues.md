# coBin Linear Issue Backlog

Linear tools were not available in this Codex session, so this file is the source list to import into Linear.

## Project

- Use existing project if present: `coBin`
- Otherwise create: `coBin 안정화 및 운영 준비`
- Default status: `Todo`

## Issues

### P0 security: Remove hardcoded secrets and rotate exposed credentials

Labels: `security`, `backend`, `desktop`

Description:
Move Django, Gmail, Twilio, GitHub, and Firebase credentials out of tracked source. Rotate all previously exposed credentials.

Acceptance criteria:
- No real PAT, app password, Twilio token, Django secret, or Firebase admin JSON remains in tracked files.
- Runtime reads secrets from environment variables.
- `.env.example` documents required variables.
- Previously exposed credentials are revoked and reissued outside Git.

### P0 bug: Restore Python compile health

Labels: `bug`, `backend`, `desktop`

Description:
Fix syntax errors that prevent static compilation across `cobin` and `desktop_app`.

Acceptance criteria:
- `python -m compileall -q cobin desktop_app` passes.

### P0 backend: Stabilize Django configuration and routing

Labels: `backend`, `bug`

Description:
Remove duplicate root routing, fix WebSocket parameter mismatch, avoid import-time Firebase crashes, and fix redirects with missing route params.

Acceptance criteria:
- Django imports without a Firebase credential file.
- Root URL resolves through `views.home`.
- `ws/points/<username>/` matches `PointConsumer`.
- `update_post_status` redirects with both category and pk.

### P1 backend: Verify auth, purchase, point, and notification APIs

Labels: `backend`, `testing`

Description:
Cover JWT-authenticated APIs, point purchase/consumption, Firestore sync, and WebSocket point update behavior.

Acceptance criteria:
- Authenticated point update adjusts local profile points.
- Firestore configured path updates remote user document.
- Firestore missing path fails gracefully or no-ops where appropriate.
- WebSocket group notification payload is stable.

### P1 desktop: Stabilize login and server integration

Labels: `desktop`, `bug`

Description:
Validate desktop login, JWT calls, `SURVER_URL`, and behavior when the local server is unavailable.

Acceptance criteria:
- Server running: login reaches the main window.
- Server unavailable: user sees a clear error and the app does not crash.
- `MainWindow` construction matches call sites.

### P1 trading: Validate strategy save/load and backtesting

Labels: `desktop`, `trading`, `testing`

Description:
Exercise default/custom strategy JSON, condition/action registries, order value validation, and backtest result display.

Acceptance criteria:
- Default strategy loads without exceptions.
- Custom strategy saves and reloads.
- Backtest creates readable results and logs.
- Invalid order amount/quantity is rejected before API calls.

### P1 desktop: Harden GitHub release update flow

Labels: `desktop`, `security`

Description:
Remove mandatory GitHub PAT usage and ensure update failure does not corrupt the launcher or app executable.

Acceptance criteria:
- Public release metadata can be read without a token.
- Optional `GITHUB_TOKEN` is used only when configured.
- Failed download leaves existing executable intact.

### P2 testing: Replace manual scripts with automated tests

Labels: `testing`, `backend`

Description:
Convert ad hoc API request code into Django tests for models, views, and core API paths.

Acceptance criteria:
- `python manage.py test` runs from `cobin`.
- Model access rules and basic views are covered.
- API tests are added for authenticated point flows.

### P2 cleanup: Normalize encoding, docs, and debug artifacts

Labels: `cleanup`

Description:
Fix mojibake in comments/UI strings/docs and keep generated debug output out of source.

Acceptance criteria:
- README and UI strings render as UTF-8 Korean.
- Debug HTML output is not tracked.
- Patch notes/resources are referenced by stable paths.

### P2 triage: Import local in-progress posts as Linear issues

Labels: `needs-triage`, `backend`

Source: `cobin/db_copy.sqlite3`

Candidates:
- id `9`, title `4132432432`, category `bug`, status `in_progress`, author `brunch`, created `2025-05-07 00:31:53`, body `fdasfdasfad`
- id `8`, title `12342번 일반유저 버그 게시글입니다.`, category `bug`, status `in_progress`, author `chess`, created `2025-04-24 02:11:21`, body `ㄴㅇㅁㅇㄴㅌㅊㅈㅁㄾㅊ`
- id `7`, title `4번 버그 게시글입니다.`, category `bug`, status `in_progress`, author `brunch`, created `2025-04-24 02:06:06`, body `ㅂㅈㄱㄷㅈㅂㄱㅁㄴㅌㅋㅍ`
- id `3`, title `💸 자동매매로 수익 내는 개꿀팁 대방출! 💸`, category `free`, status `in_progress`, author `brunch`, created `2025-04-22 01:25:52`, body `asdfasdfdafdssdf`

Acceptance criteria:
- Each candidate is imported or explicitly closed as test data.
- Low-signal entries keep `needs-triage`.
