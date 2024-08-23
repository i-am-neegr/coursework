from datetime import datetime
from unittest.mock import patch

import pandas as pd

from src.home_page import generate_response


@patch("pandas.read_excel")
@patch("src.home_page.get_currency_rates")
@patch("src.home_page.get_stock_prices")
@patch("os.getenv")
def test_generate_response(
    mock_getenv, mock_get_stock_prices, mock_get_currency_rates, mock_read_excel
):
    # Mock the environment variables for the API keys
    mock_getenv.side_effect = lambda key: (
        "fake_api_key" if key in ["CURRENCY_API_KEY", "STOCK_API_KEY"] else None
    )

    # Mock DataFrame containing all necessary columns
    mock_df = pd.DataFrame(
        {
            "Дата операции": ["2024-08-01", "2024-08-02"],
            "Дата платежа": ["2024-08-01", "2024-08-02"],
            "Номер карты": ["1234", "5678"],
            "Статус": ["Completed", "Pending"],
            "Сумма операции": [150.0, 200.0],
            "Валюта операции": ["RUB", "RUB"],
            "Сумма платежа": [150.0, 200.0],
            "Валюта платежа": ["RUB", "RUB"],
            "Кэшбэк": [1.5, 2.0],
            "Категория": ["Food", "Transport"],
            "MCC": ["5411", "4121"],
            "Описание": ["Lunch", "Bus fare"],
            "Бонусы (включая кэшбэк)": [1.5, 2.0],
            "Округление на инвесткопилку": [0.0, 0.0],
            "Сумма операции с округлением": [150.0, 200.0],
        }
    )

    # Update the side effect to return the mock DataFrame
    mock_read_excel.side_effect = lambda file_path: mock_df

    # Mock the return values for currency rates and stock prices
    mock_get_currency_rates.return_value = {"USD": 74.0, "EUR": 85.0}
    mock_get_stock_prices.return_value = [{"stock": "S&P 500", "price": 4500.0}]

    # Define a specific date and time for consistent results
    test_date = datetime(2024, 8, 16, 14, 0)

    # Call the function with the file path
    result = generate_response(file_path="fake_path.xlsx", date=test_date)

    # Assertions to check if the result is as expected
    assert isinstance(result, dict), "Result should be a dictionary"

    # Check if 'cards' is in result and its content
    assert "cards" in result

    # Check if 'top_transactions' is in result and its content
    assert "top_transactions" in result

    # Further assertions to validate content
    assert len(result["cards"]) == 2, "There should be 2 cards"
    assert len(result["top_transactions"]) == 2, "There should be 2 top transactions"

    # Individual field checks

    assert result["cards"][0]["last_digits"] == "1234"
    assert result["top_transactions"][0]["date"] == "2024-08-02"
