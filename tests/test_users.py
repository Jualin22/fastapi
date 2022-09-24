import jwt
import pytest

from app import schemas
from app.config import settings
from jose import jwt


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to my API"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"mail": "Test.User4@gmail.com", "password": "password4"}
    )

    new_user = schemas.UserResponse(**res.json())
    assert new_user.mail == "Test.User4@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["mail"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")
    assert id == int(test_user["id"])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("mail, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, mail, password, status_code):
    res = client.post(
        "/login", data={"username": mail, "password": password}
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
