from sqlmodel import Field, Relationship
from objects.base import SQLModelExtented
from objects.enum.language import Language

class SubtitleFile(SQLModelExtented, table=True):
    language: Language = Field(primary_key=True)

    torrent_id: int = Field(primary_key=True, foreign_key="torrent.id")
    torrent: "Torrent" = Relationship(back_populates="subtitles")
