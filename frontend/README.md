# moa frontend

Vue 3 기반 노트 게시판 프론트엔드입니다. 게시글 목록, 검색, 상세 보기, 작성과 회원가입·로그인을 제공합니다.

## 실행

FastAPI를 `app` 디렉터리에서 `uvicorn main:app --reload`로 실행한 뒤:

```sh
npm install
npm run dev
```

Vite는 `/board`와 `/user` 요청을 `http://127.0.0.1:8000`으로 전달합니다. API 응답의 `{ code, message, result }` 봉투를 처리하고 로그인 쿠키를 위해 요청에 `credentials: include`를 사용합니다.

## 확인

```sh
npm test
npm run build
```
