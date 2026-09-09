from pydantic import BaseModel


class Config(BaseModel):
    database_file: str = "test.db"
    database_table: str = "excel_data"

    openai_url: str
    openai_model: str
