# moa frontend

Vue 3 기반 노트 게시판 프론트엔드입니다. 게시글 목록, 검색, 상세 보기, 작성과 회원가입·로그인을 제공합니다.

## 실행

FastAPI를 `app` 디렉터리에서 `uvicorn main:app --reload`로 실행한 뒤:

```sh
npm install
npm run dev
```

백엔드 기본 주소는 `VITE_API_BASE_URL` 한 곳에서 관리합니다. 운영 빌드는 `.env.production`의 `https://api.hhon.kro.kr`을 사용하고, `npm run build`에서 이 값이 번들에 반영됩니다. 개발 중에는 같은 환경 변수를 Vite 프록시가 사용하며, 값이 없으면 로컬 백엔드 `http://127.0.0.1:8000`을 사용합니다. API 응답의 `{ code, message, result }` 봉투를 처리하고 로그인 쿠키를 위해 요청에 `credentials: include`를 사용합니다.

## 소스 구조

애플리케이션 코드는 `src` 아래 기능별 폴더에 둡니다.

```text
src/
├── api/         # 백엔드 API와 외부 로그인 연동
├── assets/      # 전역 스타일과 정적 자산
├── components/  # 여러 화면에서 재사용하는 Vue 컴포넌트
├── router/      # URL을 화면 라우트로 해석
├── stores/      # 로그인 세션과 앱 상태
├── view/        # 화면 단위 Vue 뷰
├── App.vue      # 앱 루트
└── main.js      # 앱 초기화
```

## 확인

```sh
npm test
npm run build
```
