from datetime import datetime
from typing import List

from sqlalchemy import func
#from urllib import request
from db.hash import Hash
from sqlalchemy.orm.session import Session 
from schemas import PostLikesUpdate, UserBase, PostLikes
from db.models import DbPost, DbUser, DbPostLikes
from fastapi import HTTPException, Response, status

def create_like( request: PostLikes, db: Session):
    # Check if the specified post_id exists
    post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {request.post_id} not found')
    likes = db.query(DbPostLikes).filter(DbPostLikes.post_id ==request.post_id).first()
    user = db.query(DbPostLikes).filter(DbPostLikes.user_id ==request.user_id).first()
    if likes :
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Post with id {request.post_id} is already liked before')
    # Create the like to specified post
    new_like = DbPostLikes(
        like=True,
        post_id=request.post_id,
        user_id = request.user_id,
        created_at = datetime.now()
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

def update_like(id:int, request: PostLikesUpdate, db: Session):
    # Check if the specified post_like exists
    likes = db.query(DbPostLikes).filter(DbPostLikes.id == id).first()
    if not likes:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {likes.post_id} is not liked')
    user = user = db.query(DbPostLikes).filter(DbPostLikes.user_id == likes.user_id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Post with id {likes.post_id} is liked by another user')
    #post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
    #if not post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {request.post_id} not found')
    
    # Update the like to specified post
    if likes.like != request.like:
        likes.like = False
    
    db.commit()
    db.refresh(likes)
    return likes

def delete_like(id:int, db:Session):
   likes = db.query(DbPostLikes).filter(DbPostLikes.id == id).first()
   if not likes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post liked with id {id} is not found')
   db.delete(likes)
   db.commit()
   return Response(status_code=204)

def calculate_likes(post_id: int, db:Session):
    likes = db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id).first()
    if not likes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not liked")

    # Sum up all likes on this post
    total_likes = (
        db.query(func.count(DbPostLikes.id))  # Use count on a column (e.g., `id`)
        .filter(DbPostLikes.post_id == post_id, DbPostLikes.like == True)
        .scalar())


    return total_likes