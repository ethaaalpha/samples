from pathlib import Path

from streamlit.web import bootstrap

from excel_agent.configs import Config
from excel_agent.services.agent import ExcelAgent
from excel_agent.services.db import Database
from excel_agent.ui.app.context import context


def run_web_app(config: Config, agent: ExcelAgent, database: Database):
    context.agent = agent
    context.config = config
    context.database = database

    path = Path(__file__).parent.resolve() / "layout.py"
    bootstrap.run(str(path), False, [], {})
