import json
from datetime import datetime
from typing import Optional
from logger import setup_logging
from src.functions import time_ranging, filtering_by_date

import pandas as pd

logger = setup_logging()

def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> pd.DataFrame:
    transactions_filtered_by_3_months = filtering_by_date(transactions, date)
    if transactions_filtered_by_3_months.empty:
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет транзакций
    category_transcations = transactions_filtered_by_3_months[
        transactions_filtered_by_3_months["Категория"] == category]
    return category_transcations