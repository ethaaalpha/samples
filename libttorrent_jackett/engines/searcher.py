import requests

# see: https://developer.themoviedb.org/reference 
class Searcher():
    url: str = "https://api.themoviedb.org/3/"

    def __init__(self, tmdb_key: str):
        self.secret = tmdb_key

    def search(self, movie_name: str) -> list[str]:
        endpoint = "search/movie"
        rq = requests.get(
            f"{self.url}{endpoint}",
            params={"query": movie_name},
            headers={"Authorization": f"Bearer {self.secret}"})
        rq.raise_for_status()

        return rq.json()["results"]

    def discover(self) -> list[str]:
        endpoint = "discover/movie"
        rq = requests.get(
            f"{self.url}{endpoint}",
            headers={"Authorization": f"Bearer {self.secret}"}
        )
        rq.raise_for_status()

        return rq.json()["results"]

    def trending(self) -> list[str]:
        endpoint = "trending/movie/week"
        rq = requests.get(
            f"{self.url}{endpoint}",
            headers={"Authorization": f"Bearer {self.secret}"}
        )
        rq.raise_for_status()

        return rq.json()["results"]

    def detail(self, tmdb_id: str):
        endpoint = "movie/"
        rq = requests.get(
            f"{self.url}{endpoint}{tmdb_id}",
            headers={"Authorization": f"Bearer {self.secret}"}
        )
        rq.raise_for_status()

        return rq.json()
