from unittest.mock import Mock, patch

import pytest

from src.courses import get_currency_rates, get_stock_prices


@pytest.fixture
def mock_response():
    return {
        "Time Series (1min)": {
            "2024-08-16 16:00:00": {
                "1. open": "100.0",
                "2. high": "105.0",
                "3. low": "99.0",
                "4. close": "102.0",
                "5. volume": "1000000",
            },
            "2024-08-16 15:59:00": {
                "1. open": "101.0",
                "2. high": "104.0",
                "3. low": "98.0",
                "4. close": "101.0",
                "5. volume": "1000000",
            },
        }
    }


@patch("requests.get")
def test_get_stock_prices_with_default_stocks(mock_get, mock_response):
    # Mock the API response
    mock_get.return_value.json.return_value = mock_response

    # Call the function with a mocked API key
    result = get_stock_prices(api_key="mock_api_key")

    # Expected output
    expected_result = [{"stock": "S&P 500", "price": 102.0}]

    assert result == expected_result


@patch("requests.get")
def test_get_stock_prices_with_custom_stocks(mock_get, mock_response):
    # Mock the API response
    mock_get.return_value.json.return_value = mock_response

    # Call the function with custom stocks
    result = get_stock_prices(api_key="mock_api_key", stocks=["AAPL", "TSLA"])

    # Expected output
    expected_result = [
        {"stock": "AAPL", "price": 102.0},
        {"stock": "TSLA", "price": 102.0},
    ]

    assert result == expected_result


@patch("requests.get")
def test_get_stock_prices_with_empty_time_series(mock_get):
    # Mock the API response with empty time series
    mock_get.return_value.json.return_value = {"Time Series (1min)": {}}

    # Call the function
    result = get_stock_prices(api_key="mock_api_key", stocks=["AAPL"])

    # Expected output should be an empty list since no data is available
    assert result == []


@patch("requests.get")
def test_get_stock_prices_with_missing_time_series(mock_get):
    # Mock the API response without 'Time Series (1min)' key
    mock_get.return_value.json.return_value = {}

    # Call the function
    result = get_stock_prices(api_key="mock_api_key", stocks=["AAPL"])

    # Expected output should be an empty list since no data is available
    assert result == []


@patch("requests.get")
def test_get_currency_rates(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {
        "rates": {
            "USD": 100,
            "EUR": 100,
        }
    }

    assert get_currency_rates(api_key="ляляля три тополя нету апи у меня") == [
        {"currency": "USD", "rate": 100},
        {"currency": "EUR", "rate": 100},
    ]
