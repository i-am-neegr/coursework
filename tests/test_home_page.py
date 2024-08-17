import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd

# Import the function to be tested
from src.home_page import generate_response


@patch("pandas.read_excel")
@patch("src.home_page.get_currency_rates")
@patch("src.home_page.get_stock_prices")
@patch("os.getenv")
def test_generate_response(mock_getenv, mock_get_stock_prices, mock_get_currency_rates, mock_read_excel):
    # Mock the environment variables for the API keys
    mock_getenv.side_effect = lambda key: "fake_api_key" if key in ["CURRENCY_API_KEY", "STOCK_API_KEY"] else None

    # Mock the DataFrame returned by pd.read_excel
    mock_df_cards = pd.DataFrame({
        'Номер карты': ['*1234', '*5678'],
        'Сумма операции': [150.0, 200.0],
        'Кэшбэк': [1.5, 2.0]
    })

    mock_df_transactions = pd.DataFrame({
        'Дата платежа': ['2024-08-01', '2024-08-02'],
        'Сумма операции': [300.0, 250.0],
        'Категория': ['Фастфуд', 'Транспорт'],
        'Описание': ['Lunch', 'Bus fare']
    })

    # Mocking different calls to `read_excel`
    mock_read_excel.side_effect = lambda file_path: mock_df_cards if "cards" in file_path else mock_df_transactions

    # Mock the return values for currency rates and stock prices
    mock_get_currency_rates.return_value = {"USD": 74.0, "EUR": 85.0}
    mock_get_stock_prices.return_value = [{"stock": "S&P 500", "price": 4500.0}]

    # Define a specific date and time for consistent results
    test_date = datetime(2024, 8, 16, 14, 0)

    # Call the function
    result = generate_response("fake_transactions_path.xlsx", date=test_date)

    # Expected output
    expected_result = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": '1234', "total_spent": 150.0, "cashback": 1.5},
            {"last_digits": '5678', "total_spent": 200.0, "cashback": 2.0}
        ],
        "top_transactions": [
            {"date": '2024-08-01', "amount": 300.0, "category": 'Food', "description": 'Lunch'},
            {"date": '2024-08-02', "amount": 250.0, "category": 'Transport', "description": 'Bus fare'}
        ],
        "currency_rates": {"USD": 74.0, "EUR": 85.0},
        "sp500_price": [{"stock": "S&P 500", "price": 4500.0}]
    }

    # Assertions
    assert result == expected_result
    mock_getenv.assert_any_call("CURRENCY_API_KEY")
    mock_getenv.assert_any_call("STOCK_API_KEY")
    mock_get_currency_rates.assert_called_once_with("fake_api_key")
    mock_get_stock_prices.assert_called_once_with("fake_api_key")
    assert mock_read_excel.call_count == 2  # Ensure `read_excel` was called twice
