from multiprocessing import SimpleQueue
from pathlib import Path
import tempfile
import threading
import libtorrent as lt
import time

MIN_STREAMABLE = 10

class Downloader():
    accepted_format = ["mkv", "mp4", "webm", "av1"]

    def __init__(self):
        self.session = lt.session()
        self.queue = SimpleQueue()

    def validate_torrent(self, magnet_uri: str) -> bool:
        # check if torrent contain at least a valid format video file
        info = self._fetch_torrent_info_only(magnet_uri)
        files = {f.path: f.size for f in info.files()}
        largest_file = max(files, key=files.get)

        ext = Path(largest_file).suffix

        if ext.lower() not in self.accepted_format:
            return False
        else:
            return True
        
    def add_torrent(self, magnet_uri: str):
        self.queue.put(magnet_uri)

    def _wait_for_metadata(self, torrent_h):
        while not torrent_h.has_metadata():
            time.sleep(0.5)

    def _fetch_torrent_info_only(self, magnet_uri: str):
        # see: https://www.libtorrent.org/reference-Core.html#torrent_flags_t
        # flags like stop_when_ready are slow and fell buggy
        # so I decided to make things fast using deletable cache
        with tempfile.TemporaryDirectory() as dir:
            params = {
                'url': magnet_uri,
                'save_path': dir,
            }
            torrent_h = self.session.add_torrent(params)

            self._wait_for_metadata(torrent_h)

            torrent_info = torrent_h.get_torrent_info()
            self.session.remove_torrent(torrent_h)
            return torrent_info

    def _optimize_files(self, torrent_h):
        torrent_info = torrent_h.get_torrent_info()
        files_sizes = [f.size for f in torrent_info.files()]
        largest_file_index = files_sizes.index(max(files_sizes))

        num_files = torrent_info.num_files()
        priorities = [0] * num_files

        # only the movie should be downloaded
        priorities[largest_file_index] = 7

        torrent_h.prioritize_files(priorities)

    def _register_torrent(self, magnet_uri: str):
        # we download from magnet so we need to wait for metadata
        # this will help us prioritize only the "movie" ifle
        torrent_h = self.session.add_torrent({'url': magnet_uri, 'save_path': '.'})

        self._wait_for_metadata(torrent_h)
        self._optimize_files(torrent_h)

        torrent_s = torrent_h.status()
        print(f"starting download of {torrent_s.name} !")

    def start_thread(self):
        thread = threading.Thread(target=self.loop)
        thread.start()
        return thread

    def loop(self):
        while (True):
            # checkings actual torrents
            torrents = self.session.get_torrents()

            for tor in torrents:
                status = tor.status()

                # tor.info_hash()
                if status.is_finished:
                    print(f"torrent with name : {status.name} is finished!")
                # check if ready for stream!
                elif (status.progress * 100 > MIN_STREAMABLE):
                    print(f"torrent with name : {status.name} is ready for streaming!")
                print(f"status {status.name}: {status.progress * 100}%")
                
            # starting new torrents
            while not self.queue.empty():
                self._register_torrent(self.queue.get())
            time.sleep(1)
