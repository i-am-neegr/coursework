import logging
from logging import Logger


def setup_logging() -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        "app.log", mode="w"
    )  # Лог будет перезаписываться при каждом запуске
    file_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    return logger
