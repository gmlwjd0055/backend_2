from sqlalchemy import select
from sqlalchemy.orm import Session

from models.course import Course


_DEMO_COURSES = (
    {
        "title": "FastAPI로 만드는 첫 백엔드 API",
        "summary": "FastAPI로 빠르고 명확한 백엔드 API를 만들어 봅니다.",
        "description": "Python과 FastAPI의 기본기를 익히고 라우팅, 요청 검증, 데이터베이스 연동으로 실용적인 백엔드 API를 완성합니다.",
        "category": "백엔드",
        "thumbnail_url": None,
        "instructor_name": "강사",
        "price_krw": 79000,
        "level": "입문",
        "duration_minutes": 180,
    },
    {
        "title": "Vue 3로 시작하는 프론트엔드",
        "summary": "Vue 3의 반응형 화면 구성과 컴포넌트를 익힙니다.",
        "description": "Vue 3 컴포넌트와 반응성, 이벤트, 라우팅을 활용해 유지보수하기 좋은 프론트엔드 화면을 구현합니다.",
        "category": "프론트엔드",
        "thumbnail_url": None,
        "instructor_name": "강사",
        "price_krw": 69000,
        "level": "입문",
        "duration_minutes": 240,
    },
    {
        "title": "SQLite와 SQLAlchemy 데이터 모델링",
        "summary": "SQLite와 SQLAlchemy로 튼튼한 데이터 모델을 설계합니다.",
        "description": "SQLite 데이터베이스의 특징과 SQLAlchemy ORM을 함께 익혀 애플리케이션에 필요한 테이블과 조회를 설계합니다.",
        "category": "데이터베이스",
        "thumbnail_url": None,
        "instructor_name": "강사",
        "price_krw": 59000,
        "level": "초급",
        "duration_minutes": 150,
    },
)


def seed_demo_courses(db: Session) -> None:
    if db.scalar(select(Course.id).limit(1)) is not None:
        return
    db.add_all([Course(**course) for course in _DEMO_COURSES])
    db.commit()
