from datetime import datetime

import pandas as pd
import dotenv
import os
from src.courses import get_stock_prices, get_currency_rates

dotenv.load_dotenv()


def get_greeting(date: datetime) -> str:
    hour = date.hour

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


def generate_response(file_path: str = '..\\data\\operations.xlsx', date: datetime = datetime.now()):
    api_key_currency = os.getenv('CURRENCY_API_KEY')
    api_key_stock = os.getenv('STOCK_API_KEY')

    # Generate the JSON response
    response = {
        "greeting": get_greeting(date),
        "cards": get_card_data(file_path),
        "top_transactions": get_top_transactions(file_path),
        "currency_rates": get_currency_rates(api_key_currency),
        "sp500_price": get_stock_prices(api_key_stock)
    }
