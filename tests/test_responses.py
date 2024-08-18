import pytest
import pandas as pd
from src.responses import spending_by_category

@pytest.fixture
def sample_transactions():
    data = {
        'Дата операции': ['2024-08-01', '2024-08-02', '2024-08-02', '2024-08-03'],
        'Категория': ['Food', 'Transport', 'Food', 'Entertainment'],
        'Сумма операции': [150.0, 50.0, 200.0, 300.0],
        'Описание': ['Lunch', 'Bus fare', 'Dinner', 'Movie']
    }
    return pd.DataFrame(data)

def test_empty_dataframe():
    df = pd.DataFrame()
    result = spending_by_category(df, 'Food', '2024-08-01')
    assert result.empty, "Результат должен быть пустым DataFrame"

def test_no_transactions_on_date(sample_transactions):
    result = spending_by_category(sample_transactions, 'Food', '2024-08-04')
    assert result.empty, "Результат должен быть пустым DataFrame для даты без транзакций"

def test_filtering_by_category(sample_transactions):
    result = spending_by_category(sample_transactions, 'Food', '2024-08-02')
    assert len(result) == 1
    assert (result['Категория'] == 'Food').all(), "Все транзакции должны быть в категории 'Food'"

def test_filtering_by_date(sample_transactions):
    result = spending_by_category(sample_transactions, 'Transport', '2024-08-02')
    assert len(result) == 1, "Должна быть 1 транзакция для категории 'Transport' на 2024-08-02"
    assert result.iloc[0]['Категория'] == 'Transport', "Категория должна быть 'Transport'"

def test_no_category_match(sample_transactions):
    result = spending_by_category(sample_transactions, 'Utilities', '2024-08-02')
    assert result.empty, "Результат должен быть пустым, если категория не найдена"
