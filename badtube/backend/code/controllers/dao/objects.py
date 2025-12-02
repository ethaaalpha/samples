from controllers.dao.sys.base import DataService
from controllers.dao.sys.engine import SessionInj
from objects.movie import Movie, MovieResult
from objects.torrent import Torrent
from objects.comment import Comment
from objects.user import User

class MovieService(DataService[Movie]):
    model = Movie

    def to_result(self, movies: list[Movie]) -> list[MovieResult]:
        return [
            MovieResult(movie=m, seen=False) for m in movies 
        ]

def get_movie_service(session: SessionInj) -> MovieService:
    return MovieService(session)

class TorrentService(DataService[Torrent]):
    model = Torrent

def get_torrent_service(session: SessionInj) -> TorrentService:
    return TorrentService(session)

class CommentService(DataService[Torrent]):
    model = Comment

def get_comment_service(session: SessionInj) -> CommentService:
    return CommentService(session)

class UserService(DataService[User]):
    model = User

def get_user_service(session: SessionInj) -> CommentService:
    return CommentService(session)
