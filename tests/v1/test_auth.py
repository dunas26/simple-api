from fastapi.testclient import TestClient
from pytest import fixture
import tests.lib as testing
from tests.mocks.services import MockUsersService
from core.models import User
from core.dependencies import user_repository
from core.services.auth import HashService
from main import app, prefix


hash_srv = HashService()


def hashed(input: str) -> str:
    return hash_srv.hash_password(input)


base_data = [
    User(
        id=1,
        username="dwayne",
        email="dwayne@rock.com",
        password=hashed("johnson"),
    ),
    User(
        id=2,
        username="david",
        email="david@sporting.com",
        password=hashed("beckham"),
    ),
]


service = MockUsersService(test_data=base_data)


def mock_user_repository():
    yield service


def reset_data():
    service.data = base_data


app.dependency_overrides[user_repository] = mock_user_repository
client: TestClient = TestClient(app)


class BaseTest:
    @fixture(autouse=True)
    def before_each(self):
        reset_data()


class TestLogin(BaseTest):
    def test_login_route_is_active(self):
        response = client.post(prefix + "/auth/login")
        assert testing.has_been_found(response) and testing.is_allowed_method(response)

    def test_login_route_accept_email_and_password_with_200(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne@rock.com", "password": "johnson"},
        )
        assert testing.is_response_ok(response)

    def test_login_route_accept_user_and_password_with_200(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne", "password": "johnson"},
        )
        assert testing.is_response_ok(response)

    def test_login_route_invalid_login(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "not-existing-username", "password": "nopassword"},
        )
        assert testing.not_found(response)
        response = client.post(
            prefix + "/auth/login",
            json={
                "name_or_email": "notexistingemail@email.com",
                "password": "nopassword",
            },
        )
        assert testing.not_found(response)

    def test_login_route_login_correct(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne", "password": "johnson"},
        )
        assert testing.is_response_ok(response)

    def test_login_route_returns_jwt_valid_token(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne", "password": "johnson"},
        )
        assert testing.is_response_ok(response)
        token = response.json().get("token")
        assert token

    def test_login_route_returns_jwt_refresh_token(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne", "password": "johnson"},
        )
        token = response.json().get("refresh_token")
        assert token

    def test_login_route_dont_send_token_on_failed_auth(self):
        response = client.post(
            prefix + "/auth/login",
            json={"name_or_email": "dwayne", "password": "not-account-password"},
        )
        json = response.json()
        assert not "token" in json
        assert not "refresh_token" in json


class TestSignup(BaseTest):
    def test_signup_route_active(self):
        response = client.post(prefix + "/auth/signup")
        assert testing.has_been_found(response)
        assert testing.is_allowed_method(response)

    def test_signup_route_no_body_provided(self):
        response = client.post(prefix + "/auth/signup")
        assert testing.unprocessable_entity(response)

    def test_signup_route_with_signup_model(self):
        signup_data = {
            "username": "michael",
            "email": "michael@basking.com",
            "password": "jordan",
        }
        signup_response = client.post(prefix + "/auth/signup", json=signup_data)
        assert testing.is_response_ok(signup_response)
        login_data = {"name_or_email": "michael", "password": "jordan"}
        login_response = client.post(prefix + "/auth/login", json=login_data)
        assert testing.is_response_ok(login_response)
        login_data["name_or_email"] = "michael@basking.com"
        login_response = client.post(prefix + "/auth/login", json=login_data)
        assert testing.is_response_ok(login_response)

    def test_signup_route_returns_username(self):
        signup_data = {
            "username": "michael",
            "email": "michael@basking.com",
            "password": "jordan",
        }
        # Performs a signup using a simple username and password
        signup_response = client.post(prefix + "/auth/signup", json=signup_data)
        data = signup_response.json().get("data")
        username = data.get("username")
        email = data.get("email")
        assert data
        assert username == signup_data.get("username")
        assert email == signup_data.get("email")
