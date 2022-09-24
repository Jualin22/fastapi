import pytest

from app import schemas
from app.config import settings

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8897")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.id == str(test_posts[0].id)
    assert post.content == test_posts[0].content
    # assert res.status_code == 404


@pytest.mark.parametrize("title, content, published, rating", [
    ("awesome new title", "awesome new content", True, 1),
    ("awesome new pizza", "awesome pizza content", False, 2),
    ("awesome new pasta", "awesome pasta content", True, 3)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published, rating):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "rating": rating})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
        res = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content", "rating": 4})
        created_post = schemas.PostResponse(**res.json())
        assert res.status_code == 201
        assert created_post.title == "arbitrary title"
        assert created_post.content == "arbitrary content"
        assert created_post.published == True
        assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content", "rating": 4})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_one_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/677777")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id,
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id,
    }
    res = authorized_client.put("/posts/677777", json=data)
    assert res.status_code == 404