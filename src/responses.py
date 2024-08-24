import pandas as pd


def spending_by_category(transactions, category, date):
    required_columns = ["Дата операции", "Категория"]

    # Проверка наличия необходимых колонок
    if not all(col in transactions.columns for col in required_columns):
        return pd.DataFrame(columns=required_columns)

    # Преобразуем строку даты в datetime
    date = pd.to_datetime(date)

    # Фильтруем данные по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"].dt.date == date.date())
    ]

    # Проверяем, есть ли отфильтрованные транзакции
    if filtered_transactions.empty:
        return pd.DataFrame(
            columns=["Дата операции", "Категория"]
        )  # Возвращаем пустой DataFrame с нужными столбцами
    else:
        return filtered_transactions[["Дата операции", "Категория"]]
