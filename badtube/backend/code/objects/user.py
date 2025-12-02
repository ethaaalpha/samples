from sqlmodel import Field
from objects.base import SQLModelExtented
from objects.enum.language import Language

class User(SQLModelExtented, table=True):
    id: str = Field(primary_key=True)
    lang: Language = Language.EN
    profile_picture: str | None = None
