import requests


def get_stock_prices(api_key, stocks=None):
    # stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    if stocks is None:
        stocks = ["S&P 500"]
    stock_prices = []
    base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="

    for stock in stocks:
        url = base_url + f"{stock}&interval=1min&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        # Получаем последнюю цену акции
        time_series = data.get("Time Series (1min)", {})
        if not time_series:
            continue

        latest_time = max(time_series.keys())
        latest_price = float(time_series[latest_time]["4. close"])

        stock_prices.append({"stock": stock, "price": latest_price})

    return stock_prices


def get_currency_rates(api_key):
    url = "https://api.exchangeratesapi.io/latest?base=RUB&symbols=USD,EUR"
    response = requests.get(url, headers={"apikey": api_key})
    data = response.json()

    rates = [
        {"currency": "USD", "rate": data["rates"]["USD"]},
        {"currency": "EUR", "rate": data["rates"]["EUR"]},
    ]
    return rates
