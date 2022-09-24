import pytest

from app import schemas
from app.config import settings


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[1].id, "dir": 1}
    )
    assert res.status_code == 409


def test_delete_vote_success(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[1].id, "dir": 0}
    )
    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[1].id, "dir": 0}
    )
    assert res.status_code == 409


def test_vote_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json={"post_id": 12222645451, "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts, test_vote):
    res = client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
