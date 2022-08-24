from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pasword = utils.hash_password(user.password)

    new_user = db.execute(
        """INSERT INTO users (mail, password) VALUES('%s', '%s') RETURNING * ;"""
        % (user.mail, hashed_pasword)
    ).fetchone()
    db.commit()

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.execute("""Select * from users where id=%s limit 1;""" % (id)).fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} was not found",
        )

    return user
