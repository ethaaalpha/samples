import logging
import sys
from logging import Formatter, StreamHandler


class UnderFilter(logging.Filter):
    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level


"""
This should be used in the main of the project importing the library.
Otherwise, you could also configure your own logger properties.

If you want to use the logger the best practices are to declare:
`import logging`
`logger = logging.getLogger(__name__)`
at the top of each file using a logger.
"""


def debug_logging():
    default_formatter = Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M",
    )

    console_stdout_handler = StreamHandler(sys.stdout)
    console_stdout_handler.setFormatter(default_formatter)
    console_stdout_handler.addFilter(UnderFilter(logging.WARNING))

    console_stderr_handler = StreamHandler(sys.stderr)
    console_stderr_handler.setFormatter(default_formatter)
    console_stderr_handler.setLevel(logging.ERROR)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_stdout_handler)
    root_logger.addHandler(console_stderr_handler)
    root_logger.setLevel(logging.NOTSET)
