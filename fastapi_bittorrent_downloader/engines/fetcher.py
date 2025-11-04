from pprint import pprint
import requests
import xml.etree.ElementTree as ET

# see: https://github.com/Jackett/Jackett
# see: https://torznab.github.io/spec-1.3-draft/torznab/Specification-v1.3.html
class Fetcher():
    def __init__(self, jacket_host: str, jacket_key: str):
        self.jacket_host = jacket_host
        self.secret = jacket_key

    @property
    def url(self):
        return f"http://{self.jacket_host}/api/v2.0/indexers/all/results/torznab"

    def parse_response(self, response: str) -> None | dict:
        """
        return none if not found or not available (missing mandatory keys)
        """
        mandatory_keys = ["magneturl"]
        ns = {"torznab": "http://torznab.com/schemas/2015/feed"}

        root = ET.fromstring(response)
        item = root.find(".//item")

        data = {}
        # we use xml due to torznab "recommandation" api
        for attr in item.findall(".//torznab:attr", namespaces=ns):
            data[attr.attrib.get("name")] = attr.attrib.get("value")

        pprint(data)
        if not all(k in data for k in mandatory_keys):
            return None, None
        return data.get("magneturl"), data.get("imdbid")

    def fetch_torrent(self, movie_name: str, imdbid: str) -> None | str:
        """
        return either none or the first torrent magnet url available
        """
        params = {
            "apikey": {self.secret},
            "t": "movie",
            "q": movie_name,
            "limit": 1
        }
        rq = requests.get(self.url, params=params)
        rq.raise_for_status()

        magnet, imdbid_t = self.parse_response(rq.content)

        print(f"{imdbid_t} {imdbid}")
        if imdbid_t and imdbid_t != imdbid:
            return None
        else:
            return magnet
