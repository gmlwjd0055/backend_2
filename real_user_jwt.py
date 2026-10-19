from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
app = FastAPI(title="노트 API", version="0.1.0")

class User(BaseModel):
    id: str
    pw: str

SECRET_KEY = "dslfjgkreobdgsregwdsbcxbilcjxkesfarglrwhklrejkedkgsljkldgslj"
ALGORITHM = "HS256"
users={}
sessions={}
@app.post("/user/signup")
def signup(user: User):
    if user.id in users:
        return{"message": "이미 가입한 회원입니다."}
    users[user.id] = user.pw
    return {"message": "회원 가입이 정상적으로 처리되었습니다."}
@app.post("/user/login")
def login(user: User, response: Response):
    if user.id in users:
        if users[user.id] == user.pw:
            payload = {
                "sub": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie("EN_AT",  #클라이언트 컴퓨터의 웹 브라우저의 쿠키에 설정될 이름
                                token,  #서버에서 생성한 jwt 토큰
                                httponly=True,   # 웹 브라우저에서 JS 코드로 접근하지 못하도록 하는 설정
                                secure=False,    # 웹 브라우저에서 HTTPS에서만 사용 가능하도록 하는 설정
                                samesite="lax"   # 다른 사이트에서 보내는 요청에서는 사용하지 못하도록 하는 설정
                                )
            return{"message": token}
    return {"message": "ID 또는 PW를 확인해주세요."}

@app.get("/board/list")
def list(request: Request):
    token = request.cookies.get("EN_AT")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("로그인 된 사용자", payload["sub"])
    return {"message": payload["sub"]}