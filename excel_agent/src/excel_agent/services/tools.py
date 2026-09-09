from pydantic import BaseModel

from excel_agent.services.db import Database


class AITools(BaseModel):
    """Any function of this class should be usable as an AI tool"""

    database: Database

    def write_database(self, sql_query: str):
        """
        Perform SQL write operations against the unique SQL database.
        `sql_query` represent the SQL query to perform.
        This method is only write type operations, it do not return data from the database.
        """
        return self.database.update(sql_query)

    def read_database(self, sql_query: str):
        """
        Perform SQL read operations against the unique SQL database.
        `sql_query` represent the SQL query to perform.
        This method is only read type operations, it do not update the database.
        """
        return self.database.fetch(sql_query)

    def get_table_description(self, table_name: str):
        """Return the scheme description of the provided table."""
        # see: https://system.data.sqlite.org/home/doc/dc206da59f/Doc/Extra/pragma.html
        return self.database.fetch(f"pragma table_info({table_name})")
