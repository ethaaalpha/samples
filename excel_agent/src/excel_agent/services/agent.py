import pandas as pd
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent
from pydantic_ai.models.openai import Model

from excel_agent.configs import Config
from excel_agent.services.tools import AITools


class ExcelAgent(BaseModel):
    ai_tools: AITools
    model: Model
    config: Config

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def generate_table_scheme(self, dataframe: pd.DataFrame) -> str:
        # example_data is important to help model define datatypes.
        columns_name = dataframe.columns.tolist()
        example_data = dataframe.sample(n=min(5, len(dataframe))).to_dict(
            orient="records"
        )

        prompt = f"""
        Task: Create an SQLite table named `{self.config.database_table}` using the SQL tool.

        ### Rules:
        1. **Column Names:** Keep column names exactly as provided. Wrap names containing spaces in double quotes (e.g., "column name").
        2. **Data Types:** Infer the best SQLite type (CHAR, VARCHAR, TEXT, INT, REAL, DOUBLE, FLOAT, BOOLEAN, DATE, DATETIME, TIMESTAMP, TIME, BLOB) based on the column names and sample data.
        3. **Nullability:** Handle NULL and NOT NULL correctly based on the sample data.
        4. **Output:** Execute the query using the SQL tool. Do not write any conversational text.

        ### Input Data:
        Columns:
        {columns_name}

        Sample Data:
        {example_data}
        """
        agent = Agent(
            self.model, tools=[self.ai_tools.write_database], retries={"tools": 5}
        )
        return agent.run_sync(prompt).output

    def ask(self, query: str) -> str:
        db_describe: str = self.ai_tools.get_table_description(
            self.config.database_table
        )

        agent = Agent(
            self.model,
            tools=[self.ai_tools.read_database],
            retries={"tools": 5},
            instructions=f"""
                You are a professional SQLite database assistant.

                DATABASE CONTEXT
                - Database engine: SQLite3
                - Target table: excel_data
                - Current database schema:
                {db_describe}

                Answer the user query using the SQL provided tool.
                Never return SQL into the response, always format the output.
                """,
        )

        return agent.run_sync(query).output
