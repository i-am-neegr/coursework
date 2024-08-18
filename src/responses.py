import pandas as pd
from datetime import datetime


def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> pd.DataFrame:
    # Проверка на наличие нужных колонок
    required_columns = ["Дата операции", "Категория"]
    if not all(column in transactions.columns for column in required_columns):
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет нужных колонок

    try:
        # Пробуем преобразовать дату с временем
        current_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Если времени нет, пробуем просто с датой
        current_date = datetime.strptime(date, "%Y-%m-%d")

    # Преобразование даты в формат строки для фильтрации
    date_str = current_date.strftime("%d.%m.%Y")  # Используем формат "%d.%m.%Y" для сравнения

    # Проверка и преобразование даты в данных
    if transactions['Дата операции'].dtype == 'datetime64[ns]':
        # Если данные уже в формате datetime, преобразуем в нужный формат строки для фильтрации
        transactions['Дата операции_str'] = transactions['Дата операции'].dt.strftime("%d.%m.%Y")
    else:
        # Преобразуем строки в формат datetime и затем в строку нужного формата
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format="%d.%m.%Y %H:%M:%S")
        transactions['Дата операции_str'] = transactions['Дата операции'].dt.strftime("%d.%m.%Y")

    # Фильтрация транзакций по дате
    transactions_filtered = transactions[transactions['Дата операции_str'] == date_str]

    if transactions_filtered.empty:
        return pd.DataFrame()

    # Фильтрация транзакций по категории
    category_transactions = transactions_filtered[transactions_filtered["Категория"] == category]
    return category_transactions
