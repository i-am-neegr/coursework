import json
from datetime import datetime
import pandas as pd


def get_greeting():
    current_time = datetime.now()
    hour = current_time.hour

    match hour:
        case hour if 5 <= hour < 12:
            return "Доброе утро"
        case hour if 12 <= hour < 18:
            return "Добрый день"
        case hour if 18 <= hour < 23:
            return "Добрый вечер"
        case hour if 23 <= hour < 24 or hour < 5:
            return "Доброй ночи"
        case _:
            return "Доброго времени суток"


def get_card_data(file_path):
    df_cards = pd.read_excel(file_path)

    cards = []
    for _, row in df_cards.iterrows():
        card_info = {
            "last_digits": row['Номер карты'],
            "total_spent": row['Сумма операции'],
            "cashback": row['Кэшбэк']
        }
        cards.append(card_info)

    return cards


def get_top_transactions(file_path):
    df_transactions = pd.read_excel(file_path)

    # Сортировка по сумме транзакции и выбор топ-5
    top_transactions = df_transactions.nlargest(5, 'Сумма операции')

    transactions = []
    for _, row in top_transactions.iterrows():
        transaction_info = {
            "date": row['Дата платежа'],
            "amount": row['Сумма операции'],
            "category": row['Категория'],
            "description": row['Описание']
        }
        transactions.append(transaction_info)

    return transactions


def get_currency_rates():
    rates = [
        {
            "currency": "USD",
            "rate": 73.21
        },
        {
            "currency": "EUR",
            "rate": 87.08
        }
    ]
    return rates

def get_stock_prices():
    stocks = [
        {
            "stock": "AAPL",
            "price": 150.12
        },
        {
            "stock": "AMZN",
            "price": 3173.18
        },
        {
            "stock": "GOOGL",
            "price": 2742.39
        },
        {
            "stock": "MSFT",
            "price": 296.71
        },
        {
            "stock": "TSLA",
            "price": 1007.08
        }
    ]
    return stocks

def generate_response(file_path):
    # Generate the JSON response
    response = {
        "greeting": get_greeting(),
        "cards": get_card_data(file_path),
        "top_transactions": get_top_transactions(file_path),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices()
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


# Example usage
file_path = '..\\data\\operations.xlsx'
print(generate_response(file_path))
