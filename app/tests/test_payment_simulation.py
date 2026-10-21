import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.config import settings
from core.security import createToken
from db.database import Base, get_db
from main import app
from models.course import Course


@pytest.mark.skipif(
    not os.getenv("PORTONE_SIMULATION_BASE_URL"),
    reason="Set PORTONE_SIMULATION_BASE_URL while the local Postman simulation is running",
)
def test_confirmed_payment_uses_portone_http_simulation(monkeypatch):
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
    monkeypatch.setattr(settings, "PORTONE_STORE_ID", "store-simulation")
    monkeypatch.setattr(settings, "PORTONE_CHANNEL_KEY", "channel-simulation")
    monkeypatch.setattr(settings, "PORTONE_API_SECRET", "simulation-secret")
    monkeypatch.setattr(
        settings, "PORTONE_API_BASE_URL", os.environ["PORTONE_SIMULATION_BASE_URL"]
    )
    try:
        with session_local() as db:
            db.add(
                Course(
                    id=1,
                    title="Simulation course",
                    summary="",
                    description="",
                    category="test",
                    thumbnail_url=None,
                    instructor_name="test",
                    price_krw=79000,
                    level="basic",
                    duration_minutes=60,
                )
            )
            db.commit()
        with TestClient(app) as client:
            client.cookies.set("EN_AT", createToken("simulation-buyer"))
            order = client.post("/payments/orders", json={"course_id": 1}).json()["result"]
            fixed_payment_id = "course-1-postman-simulation"
            with session_local() as db:
                from models.payment import PaymentOrder

                db.query(PaymentOrder).filter_by(payment_id=order["payment_id"]).one().payment_id = fixed_payment_id
                db.commit()

            response = client.post(
                "/payments/confirm", json={"payment_id": fixed_payment_id}
            )

        assert response.status_code == 200
        assert response.json()["result"]["status"] == "PAID"
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
