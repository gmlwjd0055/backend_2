# 기술 스택
frontend 폴더에 vue 프로젝트로 프론트엔드 개발
app 폴더에 fastapi 프로젝트로 백엔드 개발
DB는 SQLlite로 app.db 파일로 관리

# 검증
백엔드는 pytest로 테스트할 수 있는 테스트 코드 작성 후 전체 통과되면 완료
프론트엔드는 jest로 테스트할 수 있는 테스트 코드 작성 후 전체 통과되면 완료

# 서브에이전트
백엔드의 구현·디버깅·리뷰 작업은 `.codex/agents/backend-dev.toml`에 정의된 `backend_dev`를 사용한다.
프론트엔드의 구현·디버깅·리뷰 작업은 `.codex/agents/frontend-dev.toml`에 정의된 `frontend_dev`를 사용한다.
프론트엔드와 백엔드에 걸친 작업은 각 담당 에이전트에게 독립된 부분을 위임하고 결과를 조율한다.
