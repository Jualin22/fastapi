# import pytest
# from fastapi.testclient import TestClient

# import app.database as db
# from app.main import app
# from app.database import get_db, override_get_db


# def create_test_tables() -> None:
#     drop_list = [db.sql_drop_votes, db.sql_drop_posts, db.sql_drop_users]
#     create_list = [db.sql_create_users, db.sql_create_posts, db.sql_create_votes]
#     insert_list = [db.sql_insert_users, db.sql_insert_posts, db.sql_insert_votes]
#     db.run_queries(query_list=drop_list, env="test")
#     db.run_queries(query_list=create_list, env="test")
#     db.run_queries(query_list=insert_list, env="test")


# @pytest.fixture
# def session():
#     app.dependency_overrides[get_db] = override_get_db  # override dev with test
#     create_test_tables()

# @pytest.fixture
# def client(session):
#     # run our code before we run our test
#     yield TestClient(app)
#     # run our code after test finishes


# @pytest.fixture
# def test_user(client):
#     user_data = {"mail": "sanjeev@gmail.com",
#                  "password": "password123"}
#     res = client.post("/users/", json=user_data)

#     assert res.status_code == 201

#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user



    