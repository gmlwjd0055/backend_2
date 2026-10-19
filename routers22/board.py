from fastapi import APIRouter

router = APIRouter(prefix="/board", tags=["user"])

@router.get("/read")
def read():
    print("라우터를 통해서 만든 함수")
    return {"message": "라우터를 통해서 만든 /read 함수"}

@router.get("/register")
def register():
    print("라우터를 통해서 만든 함수")
    return {"message": "라우터를 통해서 만든 /register 함수"}