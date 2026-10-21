# Course Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan in the separate backend and frontend worktrees, then integrate and review the results.

**Goal:** Replace the note-centered home flow with a database-backed course catalog and detail page that show three initial course products and their prices.

**Architecture:** The backend owns the SQLAlchemy course model, idempotent demo seeding, and public read endpoints. The Vue app consumes the agreed `/courses` contract, displays the catalog at `/`, and loads course details at `/courses/{id}`. Backend and frontend work independently in separate managed worktrees; the lead integrates only scoped files into the existing checkout and runs the complete suites.

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic, SQLite, Vue 3, Jest, `@vue/test-utils`, `@vue/vue3-jest`.

**Spec:** `docs/superpowers/specs/2026-10-20-course-catalog-design.md`

## Global Constraints

- The API keeps the existing `{ code, message, result }` response envelope.
- `GET /courses` is public and returns course summary records in newest-first order.
- `GET /courses/{course_id}` is public and returns the full record, or a 404 envelope when missing.
- The initial data has exactly these demo products and prices: FastAPI, 79,000 KRW; Vue 3, 69,000 KRW; SQLite/SQLAlchemy, 59,000 KRW.
- All three demo courses use instructor name `강사`.
- No course authoring, enrollment, payment, video playback, or refund behavior is added.
- Existing login and signup routes remain available; the course catalog does not require authentication.
- Preserve all unrelated, pre-existing uncommitted changes in the primary checkout.
- Backend verification uses pytest; frontend verification uses Jest and the production Vite build.

## Review Focus

- An unknown course ID must produce a 404 envelope, not a null detail page — backend endpoint test and frontend error-state test.
- Empty catalog responses must show an intentional empty state — frontend component test.
- Repeated database initialization must not duplicate the three sample courses — backend seed idempotency test.
- A missing thumbnail or image load failure must show the same fallback without breaking card layout — frontend component tests.
- Korean currency values must render with comma grouping and the `원` suffix — frontend formatting/component test.

---

## Worktree Setup

Before dispatching either implementer:

1. Use the managed Codex worktree tool to create one worktree from the latest `main` for `backend_dev` and another separate worktree from `main` for `frontend_dev`.
2. The primary checkout contains existing uncommitted work that managed worktrees do not copy. Copy the current project instructions and each worker's scoped working files into its worktree without copying `.git`, `.env`, `.venv`, local SQLite files, caches, or dependency directories. Do not stage, reset, stash, or commit the primary checkout's pre-existing changes.
3. Backend worktree inputs: `AGENTS.md`, `.codex/`, `PROJECT_MEMORY.md` when present, `app/`, `requirements.txt`, and `requirements-test.txt` when present.
4. Frontend worktree inputs: `AGENTS.md`, `.codex/`, `PROJECT_MEMORY.md` when present, and `frontend/`.
5. Give each implementer only its worktree path and assigned task. Have them leave scoped changes available for integration; do not cherry-pick a snapshot commit over the dirty primary checkout.

## Task 1: Backend Course Data and Read API (`backend_dev` worktree)

**Files:**
- Create: `app/models/course.py`
- Create: `app/schemas/course.py`
- Create: `app/db/seed.py`
- Create: `app/api/routers/courses.py`
- Modify: `app/main.py`
- Test: `app/tests/test_courses.py`

**Interfaces:**
- Consumes: `db.database.Base`, `db.database.get_db`, and the current FastAPI response envelope.
- Produces: `seed_demo_courses(db: Session) -> None`, `GET /courses -> list[CourseSummary]`, and `GET /courses/{course_id} -> CourseDetail`.
- `CourseSummary` fields: `id: int`, `title: str`, `summary: str`, `category: str`, `thumbnail_url: str | None`, `instructor_name: str`, `price_krw: int`, `level: str`, `duration_minutes: int`.
- `CourseDetail` contains every `CourseSummary` field plus `description: str`.

- [ ] **Step 1: Write failing list, detail, 404, and seed tests**

  In `app/tests/test_courses.py`, use an in-memory SQLite engine and the existing `get_db` override pattern. Add tests named `test_course_list_returns_seeded_courses_newest_first`, `test_course_detail_returns_full_course`, `test_missing_course_returns_404_envelope`, and `test_seed_demo_courses_is_idempotent`. Assert the three exact titles/prices from the spec, the `강사` name, detail description, 404 status/envelope, and exactly three rows after calling the seeder twice. Import the seeder inside the idempotency test so the file can be collected before `app/db/seed.py` exists.

- [ ] **Step 2: Run the new tests and confirm they fail for the missing course feature**

  Run: `pytest app/tests/test_courses.py -q`
  Expected: FAIL because `/courses` is not registered and the idempotency test cannot import the not-yet-created seeder; no unrelated test-fixture errors.

- [ ] **Step 3: Implement the course model and Pydantic response schemas**

  In `app/models/course.py`, define SQLAlchemy `Course` with the spec fields. Give `price_krw` and `duration_minutes` database check constraints so they cannot be negative; allow a missing `thumbnail_url`. In `app/schemas/course.py`, define `CourseSummary` and `CourseDetail` with `ConfigDict(from_attributes=True)`.

- [ ] **Step 4: Implement idempotent demo seeding and exact sample records**

  In `app/db/seed.py`, implement `seed_demo_courses(db: Session) -> None`. Insert the three spec rows only when the course table is empty, use `강사` for every instructor, provide concise summaries and longer descriptions about the listed technologies, set thumbnail URLs to `None`, and commit once. Calling the helper again must leave the row count at three.

- [ ] **Step 5: Implement the two public read endpoints and database initialization**

  In `app/api/routers/courses.py`, add `APIRouter(prefix="/courses", tags=["courses"])`. `GET /courses` selects courses ordered by descending `id` and returns `list[CourseSummary]`. `GET /courses/{course_id}` uses `db.get`; raise `HTTPException(404, "강의를 찾을 수 없습니다.")` when missing. Import the model before `Base.metadata.create_all`, register the router in `app/main.py`, and invoke the idempotent seeder when the application initializes its configured database.

- [ ] **Step 6: Run the backend tests and confirm the API contract**

  Run: `pytest app/tests/test_courses.py -q`
  Expected: PASS with list, detail, 404 envelope, and idempotency assertions green.

- [ ] **Step 7: Commit the backend worktree changes**

  Stage only the course model, schema, seeder, router, `main.py`, and `test_courses.py`; commit as `feat: add course catalog read API`.

## Task 2: Frontend Course Catalog and Detail (`frontend_dev` worktree)

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json`
- Modify: `frontend/jest.config.cjs`
- Modify: `frontend/src/api.js`
- Modify: `frontend/src/api.test.js`
- Modify: `frontend/src/App.vue`
- Modify: `frontend/src/style.css`
- Test: `frontend/src/App.test.js`

**Interfaces:**
- Consumes: `GET /courses` summary array and `GET /courses/{id}` detail object inside the standard result envelope.
- Produces: `getCourses() -> Promise<CourseSummary[]>` and `getCourse(id: number) -> Promise<CourseDetail>` in `frontend/src/api.js`.
- A catalog card navigates to `/courses/{id}`; the root path `/` remains the catalog route.

- [ ] **Step 1: Add the Vue component Jest transformer and failing API tests**

  Add `@vue/vue3-jest@29.2.6` as a dev dependency, configure `jest.config.cjs` to transform `.vue` files, then add tests in `api.test.js` named `getCourses requests the public catalog` and `getCourse requests the selected detail`. Assert exact URLs, envelope result extraction, and backend error message propagation. The Vue Jest transformer version must match the repository's Jest 29 major version ([maintainer compatibility table](https://github.com/vuejs/vue-jest#installation)).

- [ ] **Step 2: Run the API tests and confirm they fail because course functions are missing**

  Run: `npm test -- --runTestsByPath src/api.test.js` from `frontend/`.
  Expected: FAIL on missing `getCourses` and `getCourse` exports, with Jest and the Vue transformer loading successfully.

- [ ] **Step 3: Implement course API functions by reusing the existing request helper**

  In `frontend/src/api.js`, add `getCourses = () => request('/courses')` and `getCourse = (id) => request(`/courses/${id}`)`. Keep the existing base URL, credentials, response envelope, and error handling unchanged.

- [ ] **Step 4: Write failing catalog and detail component tests**

  In `frontend/src/App.test.js`, mount `App.vue` with `@vue/test-utils` and mock the API module. Add tests named `renders course cards with formatted prices`, `filters catalog by title and category`, `shows empty catalog state`, `opens selected course detail`, `shows missing thumbnail fallback`, `shows fallback when thumbnail fails to load`, and `shows unknown detail error`. Verify comma-grouped KRW, the three course titles, filtering, route `/courses/{id}`, loading/error behavior, and fallback for both `thumbnail_url: null` and an image error event.

- [ ] **Step 5: Run component tests and confirm they fail on the existing note UI**

  Run: `npm test -- --runTestsByPath src/App.test.js` from `frontend/`.
  Expected: FAIL because the catalog/detail UI and route do not exist; no transformer or module-resolution errors.

- [ ] **Step 6: Implement the catalog and detail routes in the existing Vue app**

  In `App.vue`, make `/` load courses and match `/courses/{id}` for detail. Filter the list by case-insensitive title/summary/category search and by the selected category, with `전체` clearing the category filter. Replace note/lodging copy and cards with the course catalog, show category, summary, one instructor, and `price_krw` formatted as Korean won, and show the full description plus level and duration on details. Include loading, retryable error, empty, null-thumbnail, and failed-image placeholder states. Preserve login/signup flows, remove note creation from the visible catalog flow, and do not show a nonfunctional purchase button.

- [ ] **Step 7: Run frontend Jest and production build**

  Run: `npm test -- --runInBand` and `npm run build` from `frontend/`.
  Expected: all Jest tests pass and Vite reports a successful production build.

- [ ] **Step 8: Commit the frontend worktree changes**

  Stage only the frontend files listed for this task; commit as `feat: add course catalog views`.

## Task 3: Integration and Full Verification (primary checkout)

**Files:**
- Integrate only the scoped backend files from Task 1's worktree.
- Integrate only the scoped frontend files from Task 2's worktree.

**Interfaces:**
- Requires both task outputs to agree on all fields and endpoint paths in the spec.
- Produces a primary checkout containing the backend and frontend changes while preserving unrelated existing modifications.

- [ ] **Step 1: Compare both implementations against the spec contract**

  Confirm exact API paths, field names, envelope handling, three sample titles/prices, instructor name, and public access. Review each worktree diff and copy only the assigned files into the primary checkout; do not cherry-pick snapshot commits or touch unrelated dirty files.

- [ ] **Step 2: Run the complete backend and frontend suites**

  Run: `pytest` from `app/` and `npm test -- --runInBand` from `frontend/`.
  Expected: all pre-existing and new tests pass.

- [ ] **Step 3: Run the frontend production build and inspect final status**

  Run: `npm run build` from `frontend/`, then `git status --short` from the primary checkout.
  Expected: build succeeds; only the intended feature files are added/modified beyond the pre-existing user changes.
