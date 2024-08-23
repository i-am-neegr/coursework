import json
from unittest.mock import patch

import pytest

from src.services import simple_search


@patch("src.services.load_data")
def test_simple_search_success(mock_load_data):
    # Мокируем результат load_data
    mock_load_data.return_value = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": "-160.89",
            "Валюта операции": "RUB",
            "Сумма платежа": "-160.89",
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Супермаркеты",
            "MCC": "5411",
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": "3",
            "Округление на инвесткопилку": "0",
            "Сумма операции с округлением": "160.89",
        }
    ]

    # Вызов функции simple_search
    result = simple_search("Колхоз", file_path="dummy_path.xlsx")
    expected_result = json.dumps(
        [
            {
                "Дата операции": "31.12.2021 16:44:00",
                "Дата платежа": "31.12.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": "-160.89",
                "Валюта операции": "RUB",
                "Сумма платежа": "-160.89",
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Супермаркеты",
                "MCC": "5411",
                "Описание": "Колхоз",
                "Бонусы (включая кэшбэк)": "3",
                "Округление на инвесткопилку": "0",
                "Сумма операции с округлением": "160.89",
            }
        ],
        ensure_ascii=False,
    )

    # Проверка результата
    assert (
        result == expected_result
    ), f"Результат поиска должен совпадать с ожидаемым. Получено: {result}, Ожидалось: {expected_result}"


@patch("src.services.load_data")
def test_simple_search_no_results(mock_load_data):
    # Мокируем результат load_data
    mock_load_data.return_value = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": "-160.89",
            "Валюта операции": "RUB",
            "Сумма платежа": "-160.89",
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Супермаркеты",
            "MCC": "5411",
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": "3",
            "Округление на инвесткопилку": "0",
            "Сумма операции с округлением": "160.89",
        }
    ]

    # Вызов функции simple_search
    result = simple_search("Nonexistent", file_path="dummy_path.xlsx")
    expected_result = json.dumps([], ensure_ascii=False)

    # Проверка результата
    assert (
        result == expected_result
    ), f"Результат должен быть пустым JSON. Получено: {result}, Ожидалось: {expected_result}"


@patch("src.services.load_data")
def test_simple_search_exception(mock_load_data):
    # Настройка mock для выбрасывания исключения
    mock_load_data.side_effect = Exception("Ошибка при обработке файла")

    # Проверка того, что функция выбрасывает ожидаемое исключение
    with pytest.raises(Exception, match="Ошибка при обработке файла"):
        simple_search("Lunch", file_path="dummy_path.xlsx")
