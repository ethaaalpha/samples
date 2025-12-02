import logging
from typing import Annotated
from fastapi import Depends, HTTPException
from controllers.dao.objects import CommentService, MovieService, UserService, get_comment_service, get_movie_service, get_user_service
from objects.comment import Comment
from objects.movie import Movie
from authlib.jose import JWTClaims
from objects.torrent_file import TorrentFile
from objects.user import User
from routes.tools.security import validate_token

logger = logging.getLogger(__name__)


def get_movie(movie_id: str, service: Annotated[MovieService, Depends(get_movie_service)]) -> Movie:
    movie = service.get(movie_id)

    if not movie:
        raise HTTPException(404, detail="Movie not found!")
    else:
        return movie

def get_torrent_file(movie: Annotated[Movie, Depends(get_movie)]) -> TorrentFile:
    if not movie.torrent or not movie.torrent.file:
        raise HTTPException(404, detail="Movie do not have streamable content!")
    else:
        return movie.torrent.file

def get_user_comment(comment_id: str, service: Annotated[CommentService, Depends(get_comment_service)]) -> Comment:
    # ADD USER COMMENT CHECK OWNER
    comment = service.get(comment_id)

    if not comment:
        raise HTTPException(404, detail="Comment not found!")
    else:
        return comment
    
def get_context_user(claims: Annotated[JWTClaims, Depends(validate_token)], service: Annotated[UserService, Depends(get_user_service)]):
    id = claims.get("sub")
    user = service.get(id)

    if not user:
        logger.info(f"New user: {id}")

        user = User(id=id)
        service.upsert(user)
    return user
