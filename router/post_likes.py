from db.models import DbUser
from schemas import CommentBase, PostLikes, PostLikesDisplay, PostLikesUpdate, UserAuth, UserBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_post_likes
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["likes"]
)

@router.post('/',response_model=PostLikesDisplay)
def create_like( request: PostLikes, db: Session = Depends(get_db)):
    return db_post_likes.create_like( request, db)

@router.put('/{id}', response_model=PostLikesDisplay)
def update_like(id: int,request: PostLikesUpdate, db: Session = Depends(get_db)):
    return db_post_likes.update_like(id, request, db)

@router.delete('/{id}')
def delete_like(id:int, db:Session = Depends(get_db)):
    return db_post_likes.delete_like(id, db)
