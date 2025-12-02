import logging
from typing import Annotated
from fastapi import Depends
from controllers.dao.objects import MovieService, TorrentService, get_movie_service, get_torrent_service
from controllers.external.jackett import get_jackett
from controllers.torrent.client import get_client
from controllers.external.opensubtitles import get_opensubtitles
from controllers.torrent.files import clean_torrent_directory, create_torrent_directory, get_subtitle_file
from objects.enum.language import Language
from objects.enum.status import Status
from objects.movie import Movie
from objects.subtitle import SubtitleFile
from objects.torrent import Torrent

logger = logging.getLogger(__name__)
MIN_STREAMABLE = 10

class StreamingService:
    def __init__(self, movie_service: MovieService, torrent_service: TorrentService):  # noqa: F821
        self.movie_service = movie_service
        self.torrent_service = torrent_service
        self.jackett = get_jackett()
        self.client = get_client()

    def _download_subtitles(self, movie: Movie):
        subs = get_opensubtitles()

        links = {lg: subs.find_subtitle(movie.id, lg) for lg in Language}
        for lg, link in links.items():
            if link:
                target = get_subtitle_file(movie.id, lg)

                if subs.download_subtitle(link, target):
                    file = SubtitleFile(language=lg)
                    movie.torrent.subtitles.append(file)

    def _check_missing_torrent(self, movie: Movie) -> Movie:
        if not movie.torrent:
            torrents = self.jackett.torrents(movie.title, 1)

            if len(torrents) == 0:
                return False
            else:
                movie.torrent = torrents.pop()

                self.movie_service.upsert(movie)
        return movie.torrent

    async def _start_or_resume_dl(self, movie: Movie, torrent: Torrent) -> bool:
        if torrent.file:
            if torrent.file.completed:
                logger.info("torrent already finished")
                return True
            if self.client.is_existing(torrent.url):
                logger.info("torrent already in download")
                return True

        # check if torrent valid (by checking metadata)
        torrent.file = await self.client.validate_torrent(torrent.url)
        if torrent.file:
            # everything seems to be okay for dl
            # we can prepare the directory
            create_torrent_directory(movie.id)

            self._download_subtitles(movie)
            await self.client.register_torrent(movie.id, torrent.url)
            logger.info(f"starting the download of {movie.title}")

            self.torrent_service.upsert(torrent) # save torrentfile + subsfiles
            return True
        return False

    async def play(self, movie: Movie) -> bool:
        # check if torrent existing (recall jacket one time at least)
        torrent = self._check_missing_torrent(movie)
        if not torrent:
            return False

        # try to download
        return await self._start_or_resume_dl(movie, torrent)

    def status(self, movie: Movie) -> Status:
        if not movie.torrent or not movie.torrent.file:
            return Status.NOT_REQUESTED

        torrent = movie.torrent
        file = torrent.file
        hash = self.client.str_to_hash(file.hash)

        if file.completed:
            return Status.READY

        if not self.client.is_existing(torrent.url):
            return Status.NOT_REQUESTED

        if self.client.is_torrent_finished(hash):
            file.completed = True
            self.torrent_service.upsert(torrent)

            clean_torrent_directory(id)
            return Status.READY
        
        if self.client.get_torrent_percentage(hash) >= MIN_STREAMABLE:
            return Status.READY

        logger.debug(f"actual percentage for {movie.title}: {self.client.get_torrent_percentage(hash)}%")
        return Status.REQUESTED

def get_service(movie_service: Annotated[MovieService, Depends(get_movie_service)], torrent_service: Annotated[TorrentService, Depends(get_torrent_service)]):
    return StreamingService(movie_service, torrent_service)

StreamingServiceInj = Annotated[StreamingService, Depends(get_service)]
