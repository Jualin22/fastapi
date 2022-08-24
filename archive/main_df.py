from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title post 1", "content": "content post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


def get_id_list() -> list[int]:
    id_list = [i["id"] for i in my_posts]
    return id_list


def max_id() -> int:
    id_list = get_id_list()
    id_max = max(id_list)
    return id_max


def get_index_id(id: int) -> int:
    id_list = get_id_list()
    id_index = id_list.index(id)
    return id_index


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    try:
        id_index = get_index_id(id)
        post = my_posts[id_index]
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = max_id() + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        id_index = get_index_id(id)
        my_posts.pop(id_index)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    try:
        id_index = get_index_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[id_index]=post_dict
    return{"data": post_dict}