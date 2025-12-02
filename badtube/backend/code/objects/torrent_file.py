from datetime import datetime
from sqlmodel import DateTime, Field, Relationship
from objects.base import SQLModelExtented

class TorrentFile(SQLModelExtented, table=True):
    completed: bool = False
    last_watched: datetime = Field(default_factory=datetime.now, sa_type=DateTime)
    hash: str
    ext: str

    torrent_id: int = Field(primary_key=True, foreign_key="torrent.id")
    torrent: "Torrent" = Relationship(back_populates="file")
