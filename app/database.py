from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def create_session(env: str = "test"):

    basis = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

    if env == "prod":
        SQLALCHEMY_DATABASE_URL = basis
    elif env == "test":
        SQLALCHEMY_DATABASE_URL = basis + "_test"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return Session()


def get_db():
    db = create_session(env="prod")
    try:
        yield db
    finally:
        db.close()


def override_get_db():
    db = create_session(env="test")
    try:
        yield db
    finally:
        db.close()


def run_queries(query_list: list[str], env: str = "test"):

    try:
        db = create_session(env=env)
        for s in query_list:
            db.execute(s)
            db.commit()
    finally:
        db.close()


sql_create_users = f"""
    CREATE TABLE users (
        id serial PRIMARY KEY,
        mail VARCHAR ( 50 ) UNIQUE NOT NULL,
        password VARCHAR ( 1000 ) NOT NULL,
        created_at TIMESTAMP NOT NULL default current_timestamp
    );
    """

sql_insert_users = f"""
    insert into users (mail, password) 
    values('Test.User1@gmail.com', '$2b$12$pXUVxuvw20HPbeqCZ5o0SOMoN8OV5C2x.X9mjRlxGOra.vacwl5Pu')
        ,('Test.User2@gmail.com', '$2b$12$znyqBUW2rYhXPBxXIkSw4OcFSzx.w6kuugh3QzDKx.bLwH4HM00Qq');
    """


sql_drop_users = f"""
    drop table if exists users;
    """


sql_create_posts = f"""
    CREATE TABLE posts (
        id serial PRIMARY KEY,
        title VARCHAR ( 1000 ) NOT NULL,
        content VARCHAR ( 1000 ) NOT NULL,
        rating INT,
        published BOOLEAN NOT NULL default True,
        created_at TIMESTAMP NOT NULL default current_timestamp,
        owner_id INT NOT NULL,
        FOREIGN KEY (owner_id)
            REFERENCES users (id)
    );
    """


sql_insert_posts = f"""
    insert into posts (title, content, rating, owner_id) 
    values('title post 1', 'content post 1', 2, 1)
        ,('title post 2', 'content post 2', 3, 2);
    """


sql_drop_posts = f"""
    drop table if exists posts;
    """

sql_create_votes = f"""
    CREATE TABLE votes (
        post_id INT NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (post_id)
            REFERENCES posts (id),
        FOREIGN KEY (user_id)
            REFERENCES users (id)
    );
    """

sql_insert_votes = f"""
    insert into votes (post_id, user_id) 
    values(1, 1)
        ,(1, 2);
    """

sql_drop_votes = f"""
    drop table if exists votes;
    """

# create_list=[sql_create_users, sql_create_posts, sql_create_votes]
# drop_list=[sql_drop_votes, sql_drop_posts, sql_drop_users]


# run_queries(query_list = drop_list, env = "test")
# run_queries(query_list = create_list, env = "test")
