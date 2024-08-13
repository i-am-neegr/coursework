import datetime
import json
import os
import pandas as pd

from src.responses import spending_by_category
from src.home_page import generate_response
from src.services import simple_search

if __name__ == "__main__":
    print("Главная")
    print("Введите дату в формате YYYY-MM-DD HH:MM:SS")
    user_date = datetime.datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")
    result_main_page = json.loads(generate_response(date=user_date, file_path='data\\operations.xlsx'))
    print(
        "5-0-5-0-5-4-4--4-0-4-0-4-5-5"
    )
    print("Простой поиск")
    print("Введите строку которую надо найти в описании или категории")
    line = input()
    result_services = json.loads(simple_search(line))
    print(
    """ -------0-0--------2-----2------0-0--------2-----2
        0-0-1-2-2-2-2-1--0-0-0---0-1--2-2-2-2-1--0-0-0---0-1"""
    )
    print('''Отчеты''')
    print()