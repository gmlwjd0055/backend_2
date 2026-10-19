from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/login")
def login():
    print("라우터를 통해서 만든 함수")
    return {"message": "라우터를 통해서 만든 /login 함수"}

@router.get("/signup")
def signup():
    print("라우터를 통해서 만든 함수")
    return {"message": "라우터를 통해서 만든 /signup 함수"}