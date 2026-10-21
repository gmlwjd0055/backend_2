import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base, get_db
from main import app
from models.course import Course
from models.payment import PaymentOrder
from core.security import createToken
from core.config import settings


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_local = sessionmaker(autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_course_list_returns_seeded_courses_newest_first(client):
    from db.seed import seed_demo_courses

    db = next(app.dependency_overrides[get_db]())
    try:
        seed_demo_courses(db)
    finally:
        db.close()

    response = client.get("/courses")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert [course["title"] for course in payload["result"]] == [
        "SQLite와 SQLAlchemy 데이터 모델링",
        "Vue 3로 시작하는 프론트엔드",
        "FastAPI로 만드는 첫 백엔드 API",
    ]
    assert [course["price_krw"] for course in payload["result"]] == [59000, 69000, 79000]
    assert all(course["instructor_name"] == "강사" for course in payload["result"])


def test_course_detail_returns_full_course(client):
    from db.seed import seed_demo_courses

    db = next(app.dependency_overrides[get_db]())
    try:
        seed_demo_courses(db)
        course_id = db.scalar(select(Course.id).where(Course.title == "Vue 3로 시작하는 프론트엔드"))
    finally:
        db.close()

    response = client.get(f"/courses/{course_id}")

    assert response.status_code == 200
    course = response.json()["result"]
    assert course["title"] == "Vue 3로 시작하는 프론트엔드"
    assert course["description"]
    assert course["category"] == "프론트엔드"
    assert course["duration_minutes"] == 240


def test_missing_course_returns_404_envelope(client):
    response = client.get("/courses/999999")

    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "강의를 찾을 수 없습니다.",
        "result": None,
    }


def test_seed_demo_courses_is_idempotent():
    from db.seed import seed_demo_courses

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_local = sessionmaker(autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        seed_demo_courses(db)
        seed_demo_courses(db)
        assert db.scalar(select(func.count()).select_from(Course)) == 3
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_payment_order_requires_login_and_uses_course_price(client, monkeypatch):
    from db.seed import seed_demo_courses

    monkeypatch.setattr(settings, "PORTONE_STORE_ID", "store-test")
    monkeypatch.setattr(settings, "PORTONE_CHANNEL_KEY", "channel-test")
    db = next(app.dependency_overrides[get_db]())
    try:
        seed_demo_courses(db)
        course = db.scalar(select(Course).where(Course.title == "FastAPI로 만드는 첫 백엔드 API"))
        course_id = course.id
        expected_price = course.price_krw
    finally:
        db.close()

    response = client.post("/payments/orders", json={"course_id": course_id})
    assert response.status_code == 401

    client.cookies.set("EN_AT", createToken("buyer@example.com"))
    response = client.post("/payments/orders", json={"course_id": course_id, "amount_krw": 1})
    assert response.status_code == 200
    order = response.json()["result"]
    assert order["amount_krw"] == expected_price
    assert order["store_id"] == "store-test"
    assert order["channel_key"] == "channel-test"
    assert order["payment_id"].startswith(f"course-{course_id}-")


def test_payment_confirmation_verifies_portone_amount_and_is_idempotent(client, monkeypatch):
    from db.seed import seed_demo_courses
    import api.routers.payments as payments_router

    monkeypatch.setattr(settings, "PORTONE_STORE_ID", "store-test")
    monkeypatch.setattr(settings, "PORTONE_CHANNEL_KEY", "channel-test")
    monkeypatch.setattr(settings, "PORTONE_API_SECRET", "server-secret")
    db = next(app.dependency_overrides[get_db]())
    try:
        seed_demo_courses(db)
        course = db.scalar(select(Course).where(Course.title == "FastAPI로 만드는 첫 백엔드 API"))
        course_id, amount = course.id, course.price_krw
    finally:
        db.close()
    client.cookies.set("EN_AT", createToken("buyer@example.com"))
    order = client.post("/payments/orders", json={"course_id": course_id}).json()["result"]

    class FakeResponse:
        def __init__(self, body):
            self.body = body
        def raise_for_status(self):
            return None
        def json(self):
            return self.body

    calls = []
    def fake_get(url, headers, timeout):
        calls.append((url, headers, timeout))
        return FakeResponse({"id": order["payment_id"], "status": "PAID", "currency": "KRW", "amount": {"total": amount}})
    monkeypatch.setattr(payments_router.requests, "get", fake_get)

    response = client.post("/payments/confirm", json={"payment_id": order["payment_id"]})
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "PAID"
    assert calls[0][1]["Authorization"] == "PortOne server-secret"

    client.post("/payments/confirm", json={"payment_id": order["payment_id"]})
    assert len(calls) == 1


def test_payment_confirmation_rejects_amount_mismatch(client, monkeypatch):
    from db.seed import seed_demo_courses
    import api.routers.payments as payments_router

    monkeypatch.setattr(settings, "PORTONE_STORE_ID", "store-test")
    monkeypatch.setattr(settings, "PORTONE_CHANNEL_KEY", "channel-test")
    monkeypatch.setattr(settings, "PORTONE_API_SECRET", "server-secret")
    db = next(app.dependency_overrides[get_db]())
    try:
        seed_demo_courses(db)
        course_id = db.scalar(select(Course.id).where(Course.title == "FastAPI로 만드는 첫 백엔드 API"))
    finally:
        db.close()
    client.cookies.set("EN_AT", createToken("buyer@example.com"))
    order = client.post("/payments/orders", json={"course_id": course_id}).json()["result"]

    class FakeResponse:
        def raise_for_status(self):
            return None
        def json(self):
            return {"id": order["payment_id"], "status": "PAID", "currency": "KRW", "amount": {"total": 1}}
    monkeypatch.setattr(payments_router.requests, "get", lambda *args, **kwargs: FakeResponse())

    response = client.post("/payments/confirm", json={"payment_id": order["payment_id"]})
    assert response.status_code == 400
    assert response.json()["message"] == "결제 금액 또는 상태를 확인할 수 없습니다."
