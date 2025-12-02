import logging
from typing import Annotated
from fastapi import Depends
from controllers.dao.objects import MovieService, get_movie_service
from controllers.external.jackett import get_jackett
from controllers.external.themoviedb import get_tmdb
from objects.movie import MovieResult

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, movie_service: MovieService):
        self.movie_service = movie_service

    def query(self, movie_name: str, page: int) -> list[MovieResult]:
        tmdb = get_tmdb()
        jackett = get_jackett()
        results = []

        if movie_name:
            movies = tmdb.search(movie_name, page)
        else:
            movies = tmdb.discover(page)

        for movie in movies:
            existing = self.movie_service.get(movie.id)

            if existing and existing.torrent:
                # movie & torrent already existing (but can be dead)
                results.append(existing)
            else:
                torrents = jackett.torrents(movie.title)

                if len(torrents) == 0:
                    # films with no torrents available are ignored
                    continue
                else:
                    # since we use a relationship: movie <-> torrent
                    # it will automaticly create and associate the object
                    movie.torrent = torrents.pop()
                    self.movie_service.upsert(movie)
    
                    results.append(movie)
        return self.movie_service.to_result(results)

def get_service(movie_service: Annotated[MovieService, Depends(get_movie_service)]):
    return SearchService(movie_service)

SearchServiceInj = Annotated[SearchService, Depends(get_service)]
