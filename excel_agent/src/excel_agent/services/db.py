import logging
import sqlite3
from contextlib import contextmanager
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Database(BaseModel):
    database_file: str = Field(..., description="Database file used by the system.")

    def update(self, query: str) -> str:
        con = sqlite3.connect(self.database_file)

        logger.debug(f"update SQL operation: {query}")
        try:
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()

            return "SQL operation executed successfully."
        except Exception as e:
            return f"SQL operation failed: {e}"
        finally:
            con.close()

    def fetch(self, query: str) -> Any:
        con = sqlite3.connect(self.database_file)

        logger.debug(f"fetch SQL operation: {query}")
        try:
            cursor = con.cursor()
            cursor.execute(query)

            return f"{cursor.fetchall()}"
        except Exception as e:
            return f"SQL operation failed: {e}"
        finally:
            con.close()

    @contextmanager
    def get_connection(self):
        con = sqlite3.connect(self.database_file)

        yield con
        con.close()
