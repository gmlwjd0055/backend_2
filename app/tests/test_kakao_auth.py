import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base, get_db
from core.security import createToken
from main import app
from models.user import KakaoAccount


@pytest.fixture
def client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    from core.config import settings

    monkeypatch.setitem(settings.__dict__, "KAKAO_REST_API_KEY", "test-rest-key")
    monkeypatch.setitem(
        settings.__dict__,
        "KAKAO_REDIRECT_URI",
        "http://localhost:5173/login/kakao/callback",
    )
    monkeypatch.setitem(settings.__dict__, "KAKAO_CLIENT_SECRET", "test-client-secret")

    def override_get_db():
        db = TestingSessionLocal()
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


def test_kakao_login_exchanges_code_and_uses_only_provider_id_and_nickname(
    client, monkeypatch
):
    calls = []

    class KakaoResponse:
        def __init__(self, payload, status_code=200):
            self.payload = payload
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError()

        def json(self):
            return self.payload

    def fake_post(url, **kwargs):
        calls.append(("post", url, kwargs))
        return KakaoResponse({"access_token": "kakao-access-token"})

    def fake_get(url, **kwargs):
        calls.append(("get", url, kwargs))
        return KakaoResponse({"id": 81234, "kakao_account": {"profile": {"nickname": "모아"}}})

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(requests, "get", fake_get)

    response = client.post("/user/kakao-login", json={"code": "authorization-code"})

    assert response.status_code == 200
    assert response.json()["result"] == {"nickname": "모아"}
    assert response.cookies.get("EN_AT")
    assert calls[0][0] == "post"
    assert calls[0][2]["data"] == {
        "grant_type": "authorization_code",
        "client_id": "test-rest-key",
        "redirect_uri": "http://localhost:5173/login/kakao/callback",
        "code": "authorization-code",
        "client_secret": "test-client-secret",
    }
    assert calls[1][0] == "get"
    assert calls[1][2]["params"] == {"property_keys": '["kakao_account.profile"]'}
    assert "kakao_account.email" not in str(calls)


def test_cors_allows_vue_development_origin_with_credentials(client):
    response = client.options(
        "/user/kakao-login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert response.headers["access-control-allow-credentials"] == "true"
    assert "POST" in response.headers["access-control-allow-methods"]


def test_current_session_restores_kakao_nickname_from_auth_cookie(client):
    db_dependency = app.dependency_overrides[get_db]()
    db = next(db_dependency)
    db.add(KakaoAccount(kakao_id="81234", nickname="모아"))
    db.commit()
    db.close()

    client.cookies.set("EN_AT", createToken("kakao:81234"))
    response = client.get("/user/me")

    assert response.status_code == 200
    assert response.json()["result"] == {"name": "모아"}


def test_current_session_requires_a_valid_auth_cookie(client):
    response = client.get("/user/me")

    assert response.status_code == 401
    assert response.json()["message"] == "로그인이 필요합니다."


def test_kakao_login_rejects_code_when_kakao_token_exchange_fails(client, monkeypatch):
    class KakaoResponse:
        status_code = 401

        def raise_for_status(self):
            raise requests.HTTPError()

    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: KakaoResponse())

    response = client.post("/user/kakao-login", json={"code": "invalid-code"})

    assert response.status_code == 401
    assert response.json()["message"] == "카카오 로그인을 확인할 수 없습니다."


def test_kakao_login_requires_provider_id_and_nickname(client, monkeypatch):
    class KakaoResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            if "oauth/token" in self.url:
                return {"access_token": "kakao-access-token"}
            return {"id": 81234, "kakao_account": {"profile": {}}}

        def __init__(self, url):
            self.url = url

    monkeypatch.setattr(
        requests,
        "post",
        lambda url, **kwargs: KakaoResponse(url),
    )
    monkeypatch.setattr(
        requests,
        "get",
        lambda url, **kwargs: KakaoResponse(url),
    )

    response = client.post("/user/kakao-login", json={"code": "authorization-code"})

    assert response.status_code == 401
    assert response.json()["message"] == "카카오 계정 닉네임을 확인할 수 없습니다."
