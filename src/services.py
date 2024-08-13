import os
import json

from logger import setup_logging
from src.functions import excel_unpack, find_string
from pathlib import Path

logger = setup_logging()

def simple_search(search_string: str) -> str:
    try:
        file = excel_unpack(os.path.join(Path(__file__).resolve().parents[1], "data", "operations.xlsx"))
        json_file = json.dumps(find_string(file, search_string), ensure_ascii=False)
        return json_file
    except Exception as error:
        logger.error(f"There is at least: {error}")
        raise error

