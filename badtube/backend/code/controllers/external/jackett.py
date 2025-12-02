from objects.torrent import Torrent
from settings import get_settings
import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def format(func):
    def wrapper(*args, **kwargs):
        result = []
        try:
            data: list[dict] = func(*args, **kwargs)

            for item in data:
                try:
                    magnet = item.get("magneturl")
                    peers = item.get("peers")
                    seeders = item.get("seeders")

                    if None in (magnet, peers, seeders):
                        continue

                    result.append(Torrent(url=magnet, peers=peers, seeders=seeders))
                except ValueError:
                    logger.warning("Wrong torrent data format, ignoring..")
        except requests.HTTPError:
            logger.warning("Failed to make request against jackett!")
        return result
    return wrapper

# see: https://github.com/Jackett/Jackett
# see: https://torznab.github.io/spec-1.3-draft/torznab/Specification-v1.3.html
class JackettAPI():
    def __init__(self, jacket_host: str, jacket_key: str):
        self.jacket_host = jacket_host
        self.session = requests.Session()
        self.session.params.update({"apikey": jacket_key})

    @property
    def url(self):
        return f"http://{self.jacket_host}/api/v2.0/indexers/all/results/torznab"

    def _parse_to_dict(self, response: str) -> list[dict]:
        ns = {"torznab": "http://torznab.com/schemas/2015/feed"}

        root = ET.fromstring(response)
        items = root.findall(".//item")
        results = []

        for item in items:
            data = {}
            # we use xml due to torznab "recommandation" api
            for attr in item.findall(".//torznab:attr", namespaces=ns):
                data[attr.attrib.get("name")] = attr.attrib.get("value")
            results.append(data)

        return results

    @format
    def torrents(self, movie_name: str, limit: int = 1) -> list[Torrent]:
        params = {
            "t": "movie",
            "q": movie_name,
            "cat": 2000, # to exclude adult content
            "limit": limit
        }
        rq = self.session.get(self.url, params=params)
        rq.raise_for_status()

        return self._parse_to_dict(rq.content)

def get_jackett() -> JackettAPI:
    settings = get_settings()
    return JackettAPI(settings.jackett_host, settings.jackett_key)
