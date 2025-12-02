from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import Field
from controllers.dao.objects import CommentService, get_comment_service
from objects.comment import Comment
from objects.movie import Movie
from routes.tools.dependencies import get_movie, get_user_comment

router = APIRouter(prefix="/comments", tags=["comments"])
MIN_LENGTH=4
MAX_LENGTH=1024

@router.get("/")
def all() -> list[Comment]:
    pass

@router.get("/{movie_id}")
def get(movie: Annotated[Movie, Depends(get_movie)]) -> list[Comment]:
    return movie.comments

@router.post("/{movie_id}")
def post(movie: Annotated[Movie, Depends(get_movie)],
         content: Annotated[str, Field(pattern="^[^\x00-\x08\x0B-\x1F\x7F]+$", min_length=MIN_LENGTH, max_length=MAX_LENGTH)],
         service: Annotated[CommentService, Depends(get_comment_service)]):
    # retrive USER
    new_comment = Comment(content=content, author="DUMB", movie=movie)
    service.upsert(new_comment)

@router.delete("/{movie_id}")
def delete(comment: Annotated[Comment, Depends(get_user_comment)],
           service: Annotated[CommentService, Depends(get_comment_service)]):
    service.delete(comment)
