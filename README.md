
# Приложение для анализа банковских операций

Анализирует банковские операции с Excel у пользователя.


# Веб-страницы

##  Главная
_принемает на вход строку с датой и временем в формате_
YYYY-MM-DD HH:MM:SS
 _и возвращающую JSON-ответ со следующими данными:_

_Приветствие в формате_ 
"???"
, где 
???
 — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» _в зависимости от текущего времени«(Доброго времени суток», если это путешественник во времени)._
_По каждой карте:
последние 4 цифры карты;
общая сумма расходов;
кешбэк (1 рубль на каждые 100 рублей).
Топ-5 транзакций по сумме платежа.
Курс валют.
Стоимость акций из S&P500._
***
```python  
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

    return response
```
---
#### функция находится в home_page.py

#### все вспомогательные функции импортировны из этого же модуля

# Сервисы

##  Простой поиск
_Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории_
***
```python  
def simple_search(query, file_path="data.xlsx"):
    """
    Выполняет поиск по запросу в данных из Excel-файла.
    """
    try:
        data = load_data(file_path)
        results = search_by_query(query, data)
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Ошибка при обработке файла: {e}")
```
---
#### функция находится в service.py

#### все вспомогательные функции находятся в этом же модуле

# Отчеты

##  Траты по категории
_Функция принимает на вход:_

_датафрейм с транзакциями,
название категории,
опциональную дату.
Если дата не передана, то берется текущая дата._

_Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)._
***
```python  
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: str
) -> pd.DataFrame:
    # Проверка на наличие нужных колонок
    required_columns = ["Дата операции", "Категория"]
    if not all(column in transactions.columns for column in required_columns):
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет нужных колонок

    try:
        # Пробуем преобразовать дату с временем
        current_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Если времени нет, пробуем просто с датой
        current_date = datetime.strptime(date, "%Y-%m-%d")

    # Преобразование даты в формат строки для фильтрации
    date_str = current_date.strftime(
        "%d.%m.%Y"
    )  # Используем формат "%d.%m.%Y" для сравнения

    # Проверка и преобразование даты в данных
    if transactions["Дата операции"].dtype == "datetime64[ns]":
        # Если данные уже в формате datetime, преобразуем в нужный формат строки для фильтрации
        transactions["Дата операции_str"] = transactions["Дата операции"].dt.strftime(
            "%d.%m.%Y"
        )
    else:
        # Преобразуем строки в формат datetime и затем в строку нужного формата
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
        )
        transactions["Дата операции_str"] = transactions["Дата операции"].dt.strftime(
            "%d.%m.%Y"
        )

    # Фильтрация транзакций по дате
    transactions_filtered = transactions[transactions["Дата операции_str"] == date_str]

    if transactions_filtered.empty:
        return pd.DataFrame()

    # Фильтрация транзакций по категории
    category_transactions = transactions_filtered[
        transactions_filtered["Категория"] == category
    ]
    return category_transactions
```
---
#### функция находится в responses.py(я перепутал со словом reports)

#### вспомогательные функции отсутсвуют


## Appendix

Способно обрабатывать банковские операции и возвращать сумму транзакций и кэшбэк по каждой карте. Также оно может предоставлять топ 5 операций и стоимость ваших валют и акций S&P 500. Помимо этого, приложение имеет возможность искать операции в диапазоне до 3 месяцев по заданной категории


## Environment Variables

Чтобы запустить этот проект, вам нужно будет добавить следующие переменные среды в ваш env-файл

`STOCK_API_KEY`, `CURRENCY_API_KEY`


## Authors

- [@Artem Sergeev](https://github.com/i-am-neegr)
