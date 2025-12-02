from sqlmodel import SQLModel

class SQLModelExtented(SQLModel):
    def __eq__(self, other: SQLModel) -> bool:
        if type(self) is not type(other):
            return False
        return self.model_dump_json() == other.model_dump_json()
