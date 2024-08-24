import json

import pandas as pd


def load_data(file_path):
    """
    Загружает данные из Excel-файла.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке данных: {e}")


def search_by_query(query, data):
    """
    Ищет строки, где хотя бы одно из полей содержит заданный запрос.
    """
    results = []
    for row in data:
        if any(query.lower() in str(value).lower() for value in row.values()):
            results.append(row)
    return results


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
