from asyncio import sleep
from functools import cache
from queue import SimpleQueue
from pathlib import Path
from controllers.torrent.files import MOVIE_BASENAME, get_torrent_directory
from objects.torrent_file import TorrentFile
import logging
import tempfile
import libtorrent as lt

ACCEPTED_EXT = [".mkv", ".mp4", ".webm", ".av1"]

logger = logging.getLogger(__name__)

class Client():
    def __init__(self):
        self.session = lt.session()
        self.queue = SimpleQueue()

    async def validate_torrent(self, magnet_uri: str) -> TorrentFile | None:
        # check if torrent contain at least a valid format video file
        info = await self._fetch_torrent_info_only(magnet_uri)
        files = {f.path: f.size for f in info.files()}
        largest_file = max(files, key=files.get)

        ext = Path(largest_file).suffix
        hash = str(info.info_hash())

        if ext.lower() not in ACCEPTED_EXT:
            logger.warning(f"torrent not in valid format {ext.lower()}, ignoring")
            return None
        else:
            return TorrentFile(hash=hash, ext=ext)

    async def register_torrent(self, movie_id: str, magnet_uri: str):
        """
        torrent must be validated before with validate_torrent(). 
        return the torrent hash
        """
        existing = self.is_existing(magnet_uri)

        if not existing:
            # we download from magnet so we need to wait for metadata
            # this will help us prioritize only the "movie" ifle
            torrent_h = self.session.add_torrent({
                'url': magnet_uri, 
                'save_path': f"{get_torrent_directory(movie_id)}",
                'flags': lt.torrent_flags.sequential_download
                })

            await self._wait_for_metadata(torrent_h)
            self._optimize_files(torrent_h)

    def is_existing(self, magnet_uri: str) -> str:
        hash = lt.parse_magnet_uri(magnet_uri).info_hash
        torrent_h = self.session.find_torrent(hash)

        if torrent_h.is_valid():
            return str(hash)
        else:
            return None

    def get_torrent_percentage(self, torrent_hash: str) -> int | None:
        status = self._get_torrent_status(torrent_hash)

        if status:
            return status.progress * 100
        else:
            return status

    def is_torrent_finished(self, torrent_hash: str) -> bool | None:
        status = self._get_torrent_status(torrent_hash)

        if status:
            return status.is_finished
        else:
            return status

    def unregister_torrent(self, torrent_hash: str):
        torrent_h = self.session.find_torrent(torrent_hash)

        if torrent_h.is_valid():
            self.session.remove_torrent(torrent_h)

    def str_to_hash(self, hash: str):
        return lt.sha1_hash(bytes.fromhex(hash))

    def _get_torrent_status(self, torrent_hash: str):
        torrent_h = self.session.find_torrent(torrent_hash)

        if torrent_h.is_valid():
            return torrent_h.status()
        else:
            return None

    async def _wait_for_metadata(self, torrent_h):
        while not torrent_h.has_metadata():
            logger.info("torrent waiting for metadata")
            await sleep(0.25)

    async def _fetch_torrent_info_only(self, magnet_uri: str):
        # see: https://www.libtorrent.org/reference-Core.html#torrent_flags_t
        # flags like stop_when_ready are slow and feel buggy
        # so I decided to make things fast using deletable cache
        with tempfile.TemporaryDirectory() as dir:
            params = {
                'url': magnet_uri,
                'save_path': dir,
            }
            torrent_h = self.session.add_torrent(params)

            await self._wait_for_metadata(torrent_h)

            torrent_info = torrent_h.get_torrent_info()
            self.session.remove_torrent(torrent_h)
            return torrent_info

    def _optimize_files(self, torrent_h):
        torrent_info = torrent_h.get_torrent_info()
        files = [(i, v) for i, v in enumerate(torrent_info.files())]
        files_sorted = sorted(files, key=lambda x: x[1].size)
        largest = files_sorted[-1]
        largest_i = largest[0]

        num_files = torrent_info.num_files()
        priorities = [0] * num_files

        # only the movie should be downloaded
        priorities[largest_i] = 7

        torrent_h.prioritize_files(priorities)
        torrent_h.rename_file(largest_i,  f"{MOVIE_BASENAME}{Path(largest[1].path).suffix}")

@cache
def get_client():
    # singleton
    return Client()
