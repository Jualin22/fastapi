# store all fixtures in here and every module under tests package have access to it without importing conftest

import pytest
from fastapi.testclient import TestClient

import app.database as db
from app.main import app
from app.database import get_db, override_get_db
from app.oauth2 import create_access_token


def create_test_tables() -> None:
    drop_list = [db.sql_drop_votes, db.sql_drop_posts, db.sql_drop_users]
    create_list = [db.sql_create_users, db.sql_create_posts, db.sql_create_votes]
    insert_list = [db.sql_insert_users, db.sql_insert_posts, db.sql_insert_votes]
    db.run_queries(query_list=drop_list, env="test")
    db.run_queries(query_list=create_list, env="test")
    db.run_queries(query_list=insert_list, env="test")


@pytest.fixture
def session():
    app.dependency_overrides[get_db] = override_get_db  # override dev with test
    create_test_tables()


@pytest.fixture
def client(session):
    # run our code before we run our test
    yield TestClient(app)
    # run our code after test finishes


@pytest.fixture
def test_user2(client):
    user_data = {"mail": "sanjeev1@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"mail": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


# add Authorization
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


# add Authorization
@pytest.fixture
def test_posts(test_user, test_user2):

    sql_insert_posts = f"""
    insert into posts (title, content, rating, owner_id) 
    values('title post 99', 'content post 99', 2, {test_user["id"]})
        ,('title post 999', 'content post 999', 3, {test_user["id"]}) 
        ,('title post 9999', 'content post 9999', 4, {test_user2["id"]}) RETURNING*;
    """

    db_test = db.create_session(env="test")
    test_posts = db_test.execute(sql_insert_posts).fetchall()
    db_test.commit()

    return test_posts


@pytest.fixture
def test_vote(test_posts, test_user):

    sql_insert_votes = f"""
    insert into votes (post_id, user_id) 
    values({test_posts[1].id}, {test_user["id"]})
        ,({test_posts[2].id}, {test_user["id"]}) RETURNING*;
    """
    
    db_test = db.create_session(env="test")
    test_vote = db_test.execute(sql_insert_votes).fetchall()
    db_test.commit()

    return test_vote
