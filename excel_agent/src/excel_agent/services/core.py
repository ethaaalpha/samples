import io
import os

import pandas as pd

from excel_agent.services.agent import ExcelAgent
from excel_agent.services.db import Database


def ingest(agent: ExcelAgent, database: Database, excel_file_path: str | io.BytesIO):
    if os.path.exists(agent.config.database_file):
        raise FileExistsError("Database already existing, delete it before!")

    df = pd.read_excel(excel_file_path)

    agent.generate_table_scheme(df)
    with database.get_connection() as con:
        df.to_sql(agent.config.database_table, con, if_exists="append", index=False)

    print("Database created and initialized!")
