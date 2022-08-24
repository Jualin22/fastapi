from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED  # , response_model=schemas.UserResponse
)
def vote(
    vote_dict: schemas.Vote,
    current_user: str = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    user_id = current_user["id"]
    vote_dict = vote_dict.dict()

    sql_select_one_vote = (
        """select * from votes where "post_id"=%s and "user_id"=%s limit 1;"""
        % (vote_dict["post_id"], user_id)
    )
    result_vote = db.execute(sql_select_one_vote).fetchone()

    sql_select_one_post = """select * from posts where "id"=%s limit 1;""" % (
        vote_dict["post_id"]
    )
    result_post = db.execute(sql_select_one_post).fetchone()

    if not result_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote_dict['post_id']} does not exist.",
        )

    elif not result_vote and vote_dict["dir"] == 0:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post {vote_dict['post_id']} was not liked by user {user_id} yet.",
        )

    elif result_vote and vote_dict["dir"] == 1:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post {vote_dict['post_id']} was already liked by user {user_id}.",
        )

    elif not result_vote and vote_dict["dir"] == 1:

        sql_add_one = (
            """insert into votes ("post_id", "user_id") values(%s, %s) Returning *;"""
            % (vote_dict["post_id"], user_id)
        )

        vote_added = db.execute(sql_add_one).fetchone()
        db.commit()

        return {"detail": "Vote was added."}

    elif result_vote and vote_dict["dir"] == 0:

        sql_delete_one = (
            """delete from votes where "post_id"=%s and "user_id"=%s RETURNING *;"""
            % (vote_dict["post_id"], user_id)
        )

        vote_deleted = db.execute(sql_delete_one).fetchone()
        db.commit()

        return {"detail": "Vote was deleted."}
