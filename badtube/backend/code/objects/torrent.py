from sqlmodel import Field, Relationship
from objects.base import SQLModelExtented
from objects.subtitle import SubtitleFile
from objects.torrent_file import TorrentFile

class Torrent(SQLModelExtented, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str 
    peers: int
    seeders: int

    movie_id: str = Field(foreign_key="movie.id")
    movie: "Movie" = Relationship(back_populates="torrent")
    file: TorrentFile = Relationship(back_populates="torrent", cascade_delete=True)
    subtitles: list[SubtitleFile] = Relationship(back_populates="torrent", cascade_delete=True)
