import pandas as pd

from src.responses import (
    spending_by_category,
)  # Замените 'your_module' на имя вашего модуля


def test_spending_by_category_valid_data():
    # Подготовка данных
    data = {
        "Дата операции": [
            "01.08.2024 12:00:00",
            "01.08.2024 14:30:00",
            "02.08.2024 09:15:00",
        ],
        "Категория": ["Еда", "Транспорт", "Еда"],
    }
    transactions = pd.DataFrame(data)

    # Преобразование строковых дат в datetime
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Тестирование
    result = spending_by_category(transactions, "Еда", "2024-08-01 00:00:00")

    # Для отладки
    print("Result DataFrame:\n", result)

    expected_data = {
        "Дата операции": ["01.08.2024 12:00:00"],  # Ожидаем только одну запись
        "Категория": ["Еда"],
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df["Дата операции"] = pd.to_datetime(
        expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Убедитесь, что оба DataFrame имеют одинаковые столбцы
    assert list(result.columns) == list(expected_df.columns), "Столбцы не совпадают"

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_df.reset_index(drop=True)
    )


def test_spending_by_category_no_transactions():
    # Подготовка данных
    data = {
        "Дата операции": ["01.08.2024 12:00:00"],
        "Категория": ["Еда"],
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Тестирование
    result = spending_by_category(transactions, "Транспорт", "2024-08-01 00:00:00")
    expected_df = pd.DataFrame(
        columns=["Дата операции", "Категория"]
    )  # Ожидаем пустой DataFrame с нужными столбцами

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_df.reset_index(drop=True)
    )


def test_spending_by_category_missing_columns():
    # Подготовка данных без одной из нужных колонок
    data = {
        "Дата операции": ["01.08.2024 12:00:00"],  # Оставляем только "Дата операции"
    }
    transactions = pd.DataFrame(data)

    # Преобразуем строку даты в datetime
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Тестирование
    result = spending_by_category(transactions, "Еда", "2024-08-01 00:00:00")

    # Ожидаем пустой DataFrame с нужными столбцами
    expected_df = pd.DataFrame(columns=["Дата операции", "Категория"])

    # Проверка на равенство DataFrame
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_df.reset_index(drop=True)
    )


def test_spending_by_category_invalid_date_format():
    # Подготовка данных
    data = {
        "Дата операции": ["01.08.2024 12:00:00"],
        "Категория": ["Еда"],
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Тестирование с неправильным форматом даты
    result = spending_by_category(transactions, "Еда", "01-08-2024")

    # Ожидаем пустой DataFrame с нужными столбцами
    expected_df = pd.DataFrame(columns=["Дата операции", "Категория"])

    # Проверка на равенство DataFrame
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_df.reset_index(drop=True)
    )
