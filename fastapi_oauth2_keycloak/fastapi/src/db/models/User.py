from sqlmodel import Field, SQLModel

# dumb user
class User(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
