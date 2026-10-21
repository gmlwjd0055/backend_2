# Project notes for future sessions

- The user starts and stops the frontend and backend development servers themselves. Do not leave assistant-started dev servers running; stop any servers started during a session before handing back.
- Frontend API requests target `http://127.0.0.1:8000` by default. Override this with `VITE_API_BASE_URL` when needed.
- Kakao login uses the Kakao JavaScript SDK and requests only the nickname/profile permission. Kakao email is unavailable and must not be requested. Kakao accounts are separate identities keyed by Kakao ID; do not automatically link them to local accounts by email.
