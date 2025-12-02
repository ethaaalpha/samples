from datetime import date
from pydantic import BaseModel
from sqlmodel import Date, Field, Relationship

from objects.base import SQLModelExtented
from objects.torrent import Torrent
from objects.comment import Comment

class Movie(SQLModelExtented, table=True):
    id: str = Field(primary_key=True)
    title: str
    desc: str
    release_date: date = Field(sa_type=Date)
    rating: float 
    img_link: str

    torrent: Torrent | None = Relationship(back_populates="movie", cascade_delete=True)
    comments: list[Comment] = Relationship(back_populates="movie", cascade_delete=True)

class MovieResult(BaseModel):
    movie: Movie
    seen: bool
