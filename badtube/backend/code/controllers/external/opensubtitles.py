import logging
import requests

from objects.enum.language import Language
from settings import get_settings

logger = logging.getLogger(__name__)
opensub_url = "https://api.opensubtitles.com/api/v1"

# see: https://opensubtitles.stoplight.io/docs/opensubtitles-api
class OpenSubtitlesAPI():
    def __init__(self, opensubtitles_key: str, opensubtitles_app: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Api-Key": opensubtitles_key,
            "User-Agent":  f"<<{opensubtitles_app} v0.1>>",
        })

    def _search(self, tmdb_id: str, language: Language) -> list[dict]:
        request = self.session.get(
            f"{opensub_url}/subtitles",
            params={"tmdb_id": tmdb_id, "languages": language.value, "order_by": "votes"})

        if not request.ok:
            return []
        else:
            return request.json()["data"]

    def _download(self, file_id: str) -> dict | None:
        request = self.session.post(
            f"{opensub_url}/download",
            params={"file_id": file_id, "sub_format": "webvtt"}
        )

        if not request.ok:
            return None
        else:
            return request.json()
    
    def find_subtitle(self, tmdb_id: str, language: Language) -> str | None:
        """return a download link or none, if not found"""
        sc = self._search(tmdb_id, language)

        if len(sc) == 0:
            return None

        sub = sc.pop()
        dl = self._download(sub["attributes"]["files"][0]["file_id"])

        if dl:
            return dl["link"]
        else:
            return dl
    
    def download_subtitle(self, link: str, target: str) -> bool:
        request = self.session.get(link)

        if request.ok:
            try:
                with open(target, "wb") as file:
                    file.write(request.content)
                return True
            except OSError:
                logger.warning(f"Failed to write subtitle file {target}")
                return False
        return False

def get_opensubtitles() -> OpenSubtitlesAPI:
    settings = get_settings()
    return OpenSubtitlesAPI(settings.opensubtitles_key, settings.opensubtitles_app)
