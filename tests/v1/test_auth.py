from fastapi.testclient import TestClient
import tests.lib as testing
from tests.mocks.services import MockUsersService
from core.models import User
from core.dependencies import user_repository
from core.services.auth import HashService
from main import app, prefix

hash_srv = HashService()


def hashed(input: str) -> str:
    return hash_srv.hash_password(input)


def mock_user_repository():
    service = MockUsersService(
        test_data=[
            User(id=1, username="dwayne", password=hashed("johnson")),
            User(id=2, username="david", password=hashed("beckham")),
        ]
    )
    yield service


app.dependency_overrides[user_repository] = mock_user_repository
client: TestClient = TestClient(app)


def test_login_route_is_active():
    response = client.post(prefix + "/auth/login")
    assert testing.has_been_found(response) and testing.is_allowed_method(response)


def test_login_route_accept_user_and_password_with_200():
    response = client.post(
        prefix + "/auth/login", json={"username": "dwayne", "password": "johnson"}
    )
    assert testing.is_response_ok(response)


def test_login_route_invalid_login():
    response = client.post(
        prefix + "/auth/login",
        json={"username": "not-existing-username", "password": "nopassword"},
    )
    assert testing.not_found(response)


def test_login_route_login_correct():
    response = client.post(
        prefix + "/auth/login", json={"username": "dwayne", "password": "johnson"}
    )
    assert testing.is_response_ok(response)


def test_login_route_returns_jwt_valid_token():
    response = client.post(
        prefix + "/auth/login", json={"username": "dwayne", "password": "johnson"}
    )
    assert testing.is_response_ok(response)
    token = response.json().get("token")
    assert token


def test_login_route_returns_jwt_refresh_token():
    response = client.post(
        prefix + "/auth/login", json={"username": "dwayne", "password": "johnson"}
    )
    token = response.json().get("refresh_token")
    assert token


def test_login_route_dont_send_token_on_failed_auth():
    response = client.post(
        "/auth/login", json={"username": "dwayne", "password": "not-account-password"}
    )
    json = response.json()
    assert not "token" in json
    assert not "refresh_token" in json
