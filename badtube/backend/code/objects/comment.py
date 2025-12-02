from datetime import datetime
from sqlmodel import DateTime, Field, Relationship
from objects.base import SQLModelExtented

class Comment(SQLModelExtented, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    when: datetime = Field(sa_type=DateTime, default_factory=datetime.now)
    author: str

    movie_id: str = Field(foreign_key="movie.id")
    movie: "Movie" = Relationship(back_populates="comments")
