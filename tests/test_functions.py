import unittest

from src.functions import find_string, time_ranging


class Functions(unittest.TestCase):
    def test_find_string(self):
        operation = [
            {"Категория": "Food", "Описание": "Groceries"},
            {"Категория": "Transport", "Описание": "Gas"},
        ]
        string = "food"
        result = find_string(operation, string)
        self.assertEqual(result, [{"Категория": "Food", "Описание": "Groceries"}])

    def test_find_string_match_category(self):
        operations = [
            {"Категория": "Food", "Описание": "Groceries"},
            {"Категория": "Transport", "Описание": "Bus"},
        ]
        string = "Food"
        expected_data = [{"Категория": "Food", "Описание": "Groceries"}]
        result = find_string(operations, string)
        self.assertEqual(result, expected_data)

    def test_time_ranging(self):
        date = "2023-12-31 23:59:59"
        expected_data = [
            "12 31 2023",
            "12 30 2023",
            "12 29 2023",
            "12 28 2023",
            "12 27 2023",
            "12 26 2023",
            "12 25 2023",
            "12 24 2023",
            "12 23 2023",
            "12 22 2023",
            "12 21 2023",
            "12 20 2023",
            "12 19 2023",
            "12 18 2023",
            "12 17 2023",
            "12 16 2023",
            "12 15 2023",
            "12 14 2023",
            "12 13 2023",
            "12 12 2023",
            "12 11 2023",
            "12 10 2023",
            "12 09 2023",
            "12 08 2023",
            "12 07 2023",
            "12 06 2023",
            "12 05 2023",
            "12 04 2023",
            "12 03 2023",
            "12 02 2023",
            "12 01 2023",
            "11 30 2023",
            "11 29 2023",
            "11 28 2023",
            "11 27 2023",
            "11 26 2023",
            "11 25 2023",
            "11 24 2023",
            "11 23 2023",
            "11 22 2023",
            "11 21 2023",
            "11 20 2023",
            "11 19 2023",
            "11 18 2023",
            "11 17 2023",
            "11 16 2023",
            "11 15 2023",
            "11 14 2023",
            "11 13 2023",
            "11 12 2023",
            "11 11 2023",
            "11 10 2023",
            "11 09 2023",
            "11 08 2023",
            "11 07 2023",
            "11 06 2023",
            "11 05 2023",
            "11 04 2023",
            "11 03 2023",
            "11 02 2023",
            "11 01 2023",
        ]
        result = time_ranging(date, month=2)
        self.assertEqual(result, expected_data)


if __name__ == "__main__":
    unittest.main()
