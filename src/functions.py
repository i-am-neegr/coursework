from datetime import datetime, timedelta

import pandas as pd

from logger import setup_logging

logger = setup_logging()


def excel_unpack(path: str) -> list:
    return pd.read_excel(path, na_filter=False).to_dict(orient="records")


def find_string(operation: list[dict], string: str) -> list[dict]:
    new_data = []
    for item in operation:
        if string.lower() in item["Категория"].lower() or string.lower() in item["Описание"].lower():
            new_data.append(item)
    return new_data


def time_ranging(date: str, month: int = 1) -> list:
    try:
        base = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_list = []
        for _ in range(month):
            b = b1 = int(base.strftime("%m"))
            while b == b1:
                date_list.append(base.strftime("%m %d %Y"))
                base = base - timedelta(days=1)
                b = int(base.strftime("%m"))
        return date_list
    except Exception as error:
        raise error


def filtering_by_date(operations_df: pd.DataFrame, date: str) -> pd.DataFrame:
    operations = operations_df.to_dict("records")
    filtered_operations = []
    current_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    end_date = current_date - timedelta(days=90)
    for operation in operations:
        payment_date = datetime.strptime(
            str(operation["Дата операции"]), "%d.%m.%Y %H:%M:%S"
        )
        if end_date < payment_date < current_date:
            filtered_operations.append(operation)
    filtered_operations_df = pd.DataFrame(filtered_operations)
    return filtered_operations_df
