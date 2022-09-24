from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


from .. import schemas,  oauth2
from ..config import settings
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(current_user: str = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search_title: Optional[str] ="", db: Session = Depends(get_db)):

    user_id = current_user["id"]

    # sql_select_all = f"""select * from {fqn_post_table} where "owner_id"='{user_id}';""" # only show posts if user is owner of the post
    sql_select_all = f"""
        With _count_votes as (
            select 
                    "post_id"
                    ,count(*) as "votes"
            from votes
            group by
                "post_id"
        )

        select 
            a.* 
            ,b."mail"
            ,coalesce(c."votes", 0) as "votes"
        from posts a 
        left join users b 
            on a."owner_id"=b."id"
        left join _count_votes c
            on a."id"=c."post_id"
        where a."title" like '%{search_title}%' limit {limit} offset {offset}
     """

    result=db.execute(sql_select_all).fetchall()
    
    return result


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    sql_select_one = """
        With _count_votes as (
            select 
                    "post_id"
                    ,count(*) as "votes"
            from votes
            group by
                "post_id"
        )

        select 
            a.* 
            ,b."mail"
            ,coalesce(c."votes", 0) as "votes"
        from posts a 
        left join users b 
            on a."owner_id"=b."id"
        left join _count_votes c
            on a."id"=c."post_id"
        where a."id"=%s
     """ %(id)
    
    post=db.execute(sql_select_one).fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.PostCreate, current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    post_dict = post.dict()

    sql_insert = """insert into posts ("title", "content",  "rating", "owner_id") 
            VALUES('%s', '%s',%s, %s) RETURNING*;""" %(post_dict['title'], post_dict['content'], post_dict['rating'], user_id)

    post=db.execute(sql_insert).fetchone()
    db.commit()

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user_id = current_user["id"]

    sql_select_one = """select * from posts where "id"=%s limit 1;""" %(id)
    result=db.execute(sql_select_one).fetchone()


    if result:
        owner_id = result.owner_id
        if user_id == owner_id:
            sql_delete_one = """delete from posts where "id"=%s RETURNING *;""" %(id)
            result=db.execute(sql_delete_one).fetchone()
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with id {owner_id} is the owner of the post",
            )

    elif not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    current_user: str = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["id"]
    post_dict = updated_post.dict()

    result=db.execute("""select * from posts where id=%s limit 1;""" %(id)).fetchone()

    if result:

        if user_id == result.owner_id:
            if not post_dict['rating']:
                post_dict['rating']='Null'

            sql_update = """
                            update posts
                            set "title"='%s', 
                                "content"='%s', 
                                "published"=%s, 
                                "rating"=%s
                            where "id"=%s RETURNING *
                ;""" %(post_dict['title'], post_dict['content'], post_dict['published'], post_dict['rating'], id)

            post=db.execute(sql_update).fetchone()
            db.commit()

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with id {result.owner_id} is the owner of the post",
            )

    elif not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    return post
