import datetime
import json

import pandas as pd

from src.home_page import generate_response
from src.responses import spending_by_category
from src.services import simple_search


def main():
    print("Главная")
    print("Введите дату в формате YYYY-MM-DD HH:MM:SS")

    user_date_input = input()
    try:
        user_date = datetime.datetime.strptime(user_date_input, "%Y-%m-%d %H:%M:%S")
        user_date_str = user_date_input  # Передаем строку для использования в функции spending_by_category
    except ValueError:
        print("Неверный формат даты. Попробуйте снова.")
        return

    try:
        # Получаем данные для главной страницы
        result_main_page = generate_response(
            file_path="data/operations.xlsx", date=user_date
        )
        print("5-0-5-0-5-4-4--4-0-4-0-4-5-5")
        print("Главная страница:")
        print(json.dumps(result_main_page, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при генерации главной страницы: {e}")
        print("maybe you have the problems with api")

    print("Простой поиск")
    print("Введите строку, которую надо найти в описании или категории")

    search_line = input()
    try:
        result_services = simple_search(search_line, file_path="data/operations.xlsx")
        print("-------0-0--------2-----2------0-0--------2-----2")
        print("Результаты поиска:")
        print(result_services)
    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return

    print("Отчеты")
    print("Введите категорию, по которой хотите совершить поиск")

    category = input()
    try:
        # Читаем данные из файла Excel
        transactions = pd.read_excel("data\\operations.xlsx")
        # Получаем результаты по категории
        result_category = spending_by_category(transactions, category, user_date_str)
        print("Результаты по категории:")
        print(result_category.to_json(orient="records", force_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при выполнении поиска по категории: {e}")


if __name__ == "__main__":
    main()
