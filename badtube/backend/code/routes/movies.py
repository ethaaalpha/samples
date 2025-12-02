from typing import Annotated
from fastapi import APIRouter, Depends

from controllers.dao.objects import MovieService, get_movie_service
from controllers.searcher import SearchServiceInj
from objects.movie import Movie, MovieResult
from routes.tools.dependencies import get_movie

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/")
def search(service: SearchServiceInj, name: str | None = None, page: int = 1) -> list[MovieResult]:
    return service.query(name, page)

@router.get("/{movie_id}")
def movie(movie: Annotated[Movie, Depends(get_movie)], service: Annotated[MovieService, Depends(get_movie_service)]) -> MovieResult:
    return service.to_result(movie)
