import logging
import requests
from datetime import datetime
from objects.movie import Movie
from settings import get_settings

logger = logging.getLogger(__name__)
tmdb_url = "https://api.themoviedb.org/3"
tmdb_img_url = "https://image.tmdb.org/t/p/w780"

def format(func):
    def wrapper(*args, **kwargs):
        result = []
        try:
            data: list[dict] = func(*args, **kwargs)

            for item in data:
                try:
                    result.append(Movie(
                        id=str(item.get("id")),
                        title=item.get("title"),
                        desc=item.get("overview"),
                        language=item.get("original_language"),
                        release_date=datetime.strptime(item.get("release_date"), "%Y-%m-%d").date(),
                        rating=item.get("vote_average"),
                        img_link=f"{tmdb_img_url}{item.get('poster_path')}"
                    ))
                except ValueError:
                    logger.warning("Wrong movie data format, ignoring..")
        except requests.HTTPError:
            logger.warning("Failed to make request against themoviedb!")
        return result
    return wrapper

# see: https://developer.themoviedb.org/reference 
class TheMovieDBAPI():
    def __init__(self, tmdb_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {tmdb_key}",
            "Accept": "application/json"
        })

    def _get(self, endpoint: str, **kwargs):
        r = self.session.get(f"{tmdb_url}/{endpoint}", **kwargs)
        r.raise_for_status()

        return r.json()

    @format
    def search(self, movie_name: str, page: int = 1) -> list[Movie]:
        return self._get("search/movie", params={"query": movie_name, "page": page})["results"]

    @format
    def discover(self, page: int = 1) -> list[Movie]:
        return self._get("discover/movie", params={"page": page})["results"]

    @format
    def trending(self, page: int = 1) -> list[Movie]:
        return self._get("trending/movie/week", params={"page": page})["results"]

    def detail(self, tmdb_id: str): # method actually unsafe against HTTPError
        return self._get(f"movie/{tmdb_id}")

def get_tmdb() -> TheMovieDBAPI:
    return TheMovieDBAPI(get_settings().tmdb_key)
