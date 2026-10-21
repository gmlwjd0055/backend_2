#전체 서버 진입점, 객체 생성, 라우터 등록, 테이블 생성 등 전체에 대한 설정
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import user, board, courses, payments #다른 py코드 불러오기, main만 실행해주면 됨
from db.database import Base, engine, SessionLocal
from models.user import User, KakaoAccount
from models.board import Board
from models.course import Course
from models.payment import PaymentOrder
from db.seed import seed_demo_courses
app = FastAPI(title="노트 API", version="0.1.0")

# The Vue dev server can be opened with either hostname. Credentials are needed
# because the API authenticates users with the EN_AT cookie.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def response_envelope(request: Request, call_next):
    response = await call_next(request)

    # API의 JSON 응답만 감싸고 Swagger UI 및 OpenAPI 문서는 원래 형식을 유지합니다.
    if request.url.path in {"/docs", "/docs/oauth2-redirect", "/redoc", "/openapi.json"}:
        return response
    if "application/json" not in response.headers.get("content-type", ""):
        return response
    # HTTP and validation exception handlers already return the standard envelope.
    # Returning their streamed response after reading it here would consume its body.
    if response.status_code >= 400:
        return response

    body = getattr(response, "body", None)
    if body is None:
        body = b"".join([chunk async for chunk in response.body_iterator])
    if not body:
        result = None
    else:
        try:
            result = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response

    if isinstance(result, dict) and {"code", "message", "result"}.issubset(result):
        return response

    if response.status_code >= 400:
        message = result.get("detail", "요청을 처리하지 못했습니다.") if isinstance(result, dict) else "요청을 처리하지 못했습니다."
        result = {"code": response.status_code, "message": str(message), "result": None}
    else:
        result = {"code": response.status_code, "message": "success", "result": result}

    headers = dict(response.headers)
    headers.pop("content-length", None)
    headers.pop("content-type", None)
    enveloped = JSONResponse(
        content=result,
        status_code=response.status_code,
        headers=headers,
        background=response.background,
    )
    return enveloped


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": message, "result": None},
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"code": 422, "message": "요청 데이터가 올바르지 않습니다.", "result": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "서버 내부 오류가 발생했습니다.", "result": None},
    )

app.include_router(user.router)
app.include_router(board.router)
app.include_router(courses.router)
app.include_router(payments.router)
Base.metadata.create_all(bind = engine)
with SessionLocal() as db:
    seed_demo_courses(db)
@app.get("/")
def main():
    return {"message": "메인 페이지입니다."}
