from pydantic import BaseModel

from excel_agent.configs import Config
from excel_agent.services.agent import ExcelAgent
from excel_agent.services.db import Database

"""
This should be done differently since this is very ugly.
Still here only for the POC aspect of the project.
"""


class AppContext(BaseModel):
    config: Config | None = None
    agent: ExcelAgent | None = None
    database: Database | None = None


context = AppContext()
