# Project notes for future sessions

- The user starts and stops the frontend and backend development servers themselves. Do not leave assistant-started dev servers running; stop any servers started during a session before handing back.
- Production frontend is served by Nginx on the Windows host `100.100.100.11`, installed at `C:\Users\test\Downloads\nginx-1.30.5\nginx-1.30.5`.
- Production backend runs with Uvicorn on the separate Windows host `100.100.100.12`, listening on port `8000`; deployment goes into a folder named `backend` (absolute path still needs confirmation).
- Both hosts are SSH-accessible with account `test`. Never save the supplied SSH password in repository files or project memory; configure it as a GitHub Actions Secret. SSH ports should be confirmed (22 is only a default, not yet verified).
- Production frontend API base is configured in `frontend/.env.production` as `https://api.hhon.kro.kr`. Change it there to update the production build target.
- Production frontend origin is `https://www.hhon.kro.kr`, and backend origin is `https://api.hhon.kro.kr`. The backend must allow the frontend origin with credentialed CORS; auth cookies use the parent domain `hhon.kro.kr` and require HTTPS.
- Kakao login uses the Kakao JavaScript SDK and requests only the nickname/profile permission. Kakao email is unavailable and must not be requested. Kakao accounts are separate identities keyed by Kakao ID; do not automatically link them to local accounts by email.
