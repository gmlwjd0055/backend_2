from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.board import Board
from schemas.board import RegisterRes, RegisterReq, ReadRes
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.database import get_db

router = APIRouter(prefix="/board", tags=["board"])

@router.get("/read/{idx}", response_model=ReadRes)
def read(idx:int, db:Session = Depends(get_db)):
    board = db.get(Board,idx)
    return board

@router.get("/list", response_model=list[ReadRes])
def read_list(db: Session = Depends(get_db)):
    boards = db.scalars(select(Board).order_by(Board.idx.desc())).all()
    return boards

@router.post("/register", response_model=RegisterRes)
def register(req:RegisterReq, db:Session = Depends(get_db)):
    board = Board(
        title=req.title, contents=req.contents
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return board
