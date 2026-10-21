import requests
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from core.security import createToken
from db.database import get_db
from models.user import KakaoAccount, User
from schemas.user import KakaoLoginReq, KakaoLoginRes, LoginReq, LoginRes, SessionRes, SignUpReq, SignUpRes

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=SessionRes)
def current_session(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("EN_AT")
    if not token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    try:
        subject = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ).get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="로그인이 만료되었습니다.")
    if not subject:
        raise HTTPException(status_code=401, detail="로그인이 만료되었습니다.")

    if subject.startswith("kakao:"):
        account = db.scalar(
            select(KakaoAccount).where(KakaoAccount.kakao_id == subject.removeprefix("kakao:"))
        )
        if account is None:
            raise HTTPException(status_code=401, detail="로그인이 만료되었습니다.")
        return {"name": account.nickname}
    return {"name": subject}


@router.post("/kakao-login", response_model=KakaoLoginRes)
def kakao_login(req: KakaoLoginReq, res: Response, db: Session = Depends(get_db)):
    if not settings.KAKAO_REST_API_KEY:
        raise HTTPException(status_code=503, detail="카카오 로그인이 설정되지 않았습니다.")

    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": req.code,
    }
    if settings.KAKAO_CLIENT_SECRET:
        token_data["client_secret"] = settings.KAKAO_CLIENT_SECRET

    try:
        token_response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data=token_data,
            timeout=10,
        )
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
        if not access_token:
            raise requests.RequestException("Missing Kakao access token")

        profile_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"property_keys": '["kakao_account.profile"]'},
            timeout=10,
        )
        profile_response.raise_for_status()
        profile = profile_response.json()
        kakao_id = profile.get("id")
        nickname = (profile.get("kakao_account", {}).get("profile", {}).get("nickname") or "").strip()
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="카카오 로그인을 확인할 수 없습니다.",
        )

    if not kakao_id or not nickname:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="카카오 계정 닉네임을 확인할 수 없습니다.",
        )

    account = db.scalar(select(KakaoAccount).where(KakaoAccount.kakao_id == str(kakao_id)))
    if account is None:
        account = KakaoAccount(kakao_id=str(kakao_id), nickname=nickname)
        db.add(account)
    else:
        account.nickname = nickname
    db.commit()

    res.set_cookie(
        "EN_AT",
        createToken(f"kakao:{kakao_id}"),
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return {"nickname": nickname}

@router.post("/login",response_model=LoginRes)
def login(req: LoginReq, res:Response):
    print(req.email)
    print(req.password)
    user = {
        "email":req.email,
        "password":req.password,
        "name" : "user01",
        "profile" : "배고파요"
    }
    res.set_cookie("EN_AT",
                        createToken(req.email),
                        httponly=True,
                        secure=False,
                        samesite="lax"
                        )
    return user

#제어의 역전: IoC, 객체 생성이나 프로그램의 실행 흐름의 제어를 외부로 넘기는 프로그래밍 방식
#의존성 주입 :DI, 필요한 객체를 우리가 직접 생성하지 않고 외부에서 전달해주는 방식(depends)
@router.post("/signup",response_model=SignUpRes)
def signup(req: SignUpReq, db:Session = Depends(get_db)):
    # db = SessionLocal()

    user = db.scalar(select(User).where(User.email == req.email))
    if user:
        print("중복가입")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 가입된 이메일입니다.")

    newUser = User(
        email=req.email, password=req.password, name=req.name
    )
    db.add(newUser)
    db.commit()
    return req
