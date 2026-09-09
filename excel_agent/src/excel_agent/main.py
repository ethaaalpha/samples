import argparse
import logging

from pydantic_ai import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from excel_agent.configs import Config, debug_logging
from excel_agent.services.agent import ExcelAgent
from excel_agent.services.core import ingest
from excel_agent.services.db import Database
from excel_agent.services.tools import AITools
from excel_agent.ui.entrypoint import run_web_app

logger = logging.getLogger(__name__)


def ask(agent: ExcelAgent, question: str):
    print(agent.ask(query=question))


def main():
    # args parsing / cli
    parser = argparse.ArgumentParser(
        prog="Excel Agent",
        description="Agent that interact with a structured excel document using SQL conversion.",
    )
    parser.add_argument(
        "--model", required=True, help="Model of the OpenAI API compatible provider."
    )
    parser.add_argument(
        "--url", required=True, help="BaseURL of the OpenAI API compatible provider."
    )
    parser.add_argument(
        "--db_file", required=True, help="Database file location to use/create."
    )
    parser.add_argument("--debug", action="store_true", help="Active debug loggers.")

    subparsers = parser.add_subparsers(
        dest="action", required=True, help="Action to perform."
    )

    # ingest action
    ingestion_parser = subparsers.add_parser(
        "ingest",
        help="Ingest will transform the excel file into SQL database.",
    )
    ingestion_parser.add_argument("excel_file", help="Excel structured file to ingest.")

    # ask action
    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask permit to interact with the transformed data easily.",
    )
    ask_parser.add_argument("question", help="Question to ask on the excel file.")

    # web-ui action
    _ = subparsers.add_parser("ui", help="Start the WebUI.")

    args = parser.parse_args()

    if args.debug:
        debug_logging()

    # core objects
    config = Config(
        database_file=args.db_file, openai_url=args.url, openai_model=args.model
    )
    model = OpenAIChatModel(
        config.openai_model,
        provider=OpenAIProvider(base_url=config.openai_url),
        settings=ModelSettings(thinking=False, temperature=0.1),
    )
    database = Database(database_file=config.database_file)
    agent = ExcelAgent(ai_tools=AITools(database=database), model=model, config=config)

    match args.action:
        case "ingest":
            return ingest(agent, database, args.excel_file)
        case "ask":
            return ask(agent, args.question)
        case "ui":
            return run_web_app(config, agent, database)


if __name__ == "__main__":
    main()
