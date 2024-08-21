import datetime
import json
import logging
import os
import re
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.abs_paths import get_absolute_path_for_file

log_file_path = get_absolute_path_for_file("utils.log")

if os.path.exists(log_file_path):
    os.truncate(log_file_path, 0)

logger = logging.getLogger("utils.py")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s   %(name)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_main_data_from_excel(file_path: str) -> pd.DataFrame:
    """
    Принимает путь до excel файла.
    Возвращает объект DataFrame с содержимым файла.
    """
    # Если файл не существует:
    if not os.path.exists(file_path):
        logger.error(f"При попытке чтения excel-файла, он не обнаружен по пути '{file_path}'")
        raise ValueError(f"При попытке чтения excel-файла, он не обнаружен по пути '{file_path}'")

    # Если файл не соответствующего типа:
    try:
        excel_df = pd.read_excel(file_path)
    except ValueError:
        logger.error("При попытке чтения excel-файла, он содержит некорректные данные")
        raise ValueError("При попытке чтения excel-файла, он содержит некорректные данные")

    logger.debug("Чтение базовых данных из excel-файла - OK")
    logger.debug("Нормальное завершение функции read_main_data_from_excel")
    return excel_df


# df = read_main_data_from_excel("../data/operations.xlsx")
# print(df.head())
# for i in range(5):
#     print(df["Сумма операции"][i], ": ", df["Категория"][i])


def get_greeting_by_hours(hour: int) -> str:
    """
    Принимает текущее время (час).
    Возвращает строку приветствия: "Доброй ночи / Доброе утро / Добрый день / Добрый вечер"
    """
    if type(hour) is not int:
        logger.error("Параметр hour - не типа int")
        raise ValueError("Ожидался тип int.")

    if hour > 24 or hour < 0:
        logger.error("Параметр hour должен быть в диапазоне 0 - 24")
        raise ValueError("Время (час) ожидалось в диапазоне 0-24 включительно.")

    if 0 < hour <= 6:
        greeting = "Доброй ночи"
    elif hour <= 12:
        greeting = "Доброе утро"
    elif hour <= 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    logger.debug(f"Для времени '{hour}' выбрано приветствие '{greeting}'")
    return greeting


# assert get_greeting_by_hours(5) == "Доброй ночи"
# assert get_greeting_by_hours(12) == "Доброе утро"
# assert get_greeting_by_hours(14) == "Добрый день"
# assert get_greeting_by_hours(23) == "Добрый вечер"


def get_df_by_date(df: pd.DataFrame, datetime_obj: datetime.datetime) -> pd.DataFrame | None:
    """
    Принимает:  Датафрейм и объект даты/времени.
    Возвращает: новый Датафрейм,
                отфильтрованный по дате в диапазоне: Начало месяца - Входящая дата
    """
    df_by_date = pd.DataFrame(columns=list(df.keys()))

    # Фильтрация входящего датафрейма по текущему месяцу:
    for index, row in df.iterrows():
        if type(row["Дата операции"]) is not str or len(row["Дата операции"]) != len("dd.mm.yyyy hh:mm:ss"):
            continue

        # Создание объекта datetime:
        row_datetime_obj = datetime.datetime.strptime(str(row["Дата операции"]), "%d.%m.%Y %H:%M:%S")
        # day = int(row["Дата платежа"][:2])
        # month = int(row["Дата платежа"][3:5])
        # year = int(row["Дата платежа"][-4:])
        # print(day, month, year, row["Сумма операции"], "index = ", index)
        day = row_datetime_obj.day
        month = row_datetime_obj.month
        year = row_datetime_obj.year

        if year == datetime_obj.year and month == datetime_obj.month and day <= datetime_obj.day:
            # df_by_date.loc[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

            # row_dict = dict(row)
            # dict_values = row_dict.values()
            # list_values = list(dict_values)
            # if type(index) is int:
            #     df_by_date.loc[index] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

            if type(index) is int:
                df_by_date.loc[index] = list(dict(row).values())

    return df_by_date


def generate_cards_numbers_list(df: pd.DataFrame) -> list:
    """
    Принимает:  Датафрейм.
    Возвращает: Список номер карт, содержащихся в датафрейме.
    """
    if "Номер карты" not in df:
        raise ValueError("В датафрейме отсутствует столбец 'Номер карты'.")

    # Компиляция регулярного выражения:
    pattern = re.compile(r"\*\d{4}")

    cards_list = list({el for el in df["Номер карты"] if type(el) is str and pattern.fullmatch(el) is not None})
    # ["*1111", "*2222", "*3333"]

    if len(cards_list) == 0:
        raise ValueError("В датафрейме отсутствуют номера карт вида '*1234'.")
    return cards_list


def generate_cards_spendings_dict(cards_numbers_list: list, df_by_date: pd.DataFrame) -> dict:
    """
    Принимает:  Список номеров карт.
    Возвращает: Словарь с парами {"Номер карты": "траты в текущем месяце"}
    """
    # Формируем начальный словарь с нулевыми тратами:
    cards_spendings_dict = {card: 0 for card in cards_numbers_list}

    # Ищем траты для каждой карты:
    for index, row in df_by_date.iterrows():
        card = row["Номер карты"]
        trans_amount = row["Сумма операции"]
        if card in cards_numbers_list and trans_amount < 0:
            # Отнимаем отрицательную trans_amount для суммирования:
            cards_spendings_dict[card] -= trans_amount

    return cards_spendings_dict


def generate_cards_cashbacks_dict(cards_spendings_dict: dict) -> dict:
    """
    Принимает:  Словарь с {картами: тратами}.
    Возвращает: Словарь с {картами: кешбэком}.
    """
    cards_cashbacks_dict = {card: round((spending / 100), 2) for card, spending in cards_spendings_dict.items()}
    return cards_cashbacks_dict


def generate_cards_info_list(spendings: dict, cashbacks: dict) -> list[dict]:
    """
    Принимает:  Два словаря - с тратами по картам, с кешбэками по картам.
    Возвращает: Список словарей (словарь согласно ТЗ).
    """
    cards_info_list = []
    for card, spending in spendings.items():
        # if spending > 0:
        cards_info_list.append(
            {"last_digits": card[1:], "total_spent": spending, "cashback": cashbacks[card]}  # Убираем символ-звёздочку
        )
    return cards_info_list


def generate_top_five_trans_list(df_by_date: pd.DataFrame) -> list[dict[str, Any] | None]:
    """
    Принимает:  Датафрейм по текущему месяцу.
    Возвращает: Список словарей транзакций с максимальными суммами операций.
    """
    top_five_trans_list = []
    top_five_indexes = []

    # Перебор строк датафрейма 5 раз с поиском наибольших сумм операций:
    for _ in range(5):
        # Ищем макс.сумму за проход:
        max_sum = 0
        max_sum_index = None
        transaction_dict = None

        for index, row in df_by_date.iterrows():
            if index not in top_five_indexes and abs(row["Сумма операции"]) > max_sum:
                max_sum = abs(row["Сумма операции"])
                max_sum_index = index

                # При найденной max_sum, можно предварительно для неё сформировать словарь:
                transaction_dict = {
                    "date": row["Дата операции"][:10],  # Берём часть строки, т.е. "dd.mm.yyyy"
                    "amount": round(row["Сумма операции"], 2),
                    "category": row["Категория"],
                    "description": row["Описание"],
                }
        if max_sum:
            top_five_indexes.append(max_sum_index)
            top_five_trans_list.append(transaction_dict)

    return top_five_trans_list


def write_data_to_user_settings_json(data_dict: dict) -> None:
    """
    Принимает:  Словарь с данными по акциям и валютам.
    Записывает данные в user_settings.json файл.
    """

    # Запись данных о валютах и акциях в json-файл:
    # currencies_and_stocks_dict = {
    #     "user_currencies": ["USD", "EUR"],
    #     "user_stocks": ["AAPL", "AMZN"]
    # }
    if __name__ == "__main__":
        file_path = "../user_settings.json"
    else:
        file_path = "./user_settings.json"
    # Если файл не существует:
    # if not os.path.exists(file_path):
    #     raise ValueError("Файл user_settings.json не найден.")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data_dict, file)


def get_currencies_from_user_file() -> list:
    """Возвращает список с валютами из user_settings.json файла."""

    # file_path = "../user_settings.json"
    if __name__ == "__main__" or __name__ == "utils":
        file_path = "../user_settings.json"
    else:
        file_path = "./user_settings.json"

    # Если файл не существует:
    # if not os.path.exists(file_path):
    #     raise ValueError("Файл user_settings.json не найден.")

    with open(file_path, "r", encoding="utf-8") as file:
        json_data_dict = json.load(file)

    if type(json_data_dict) is dict and "user_currencies" in json_data_dict:
        if type(json_data_dict["user_currencies"]) is list:
            return json_data_dict["user_currencies"]
    return []


def generate_rates_dicts_with_api(user_currencies_list: list) -> list[dict]:
    """
    Принимает:  Список с валютами.
    Возвращает: Список со словарями вида {"currency": "GBP", "rate": 114.53}
    """
    rates_dicts_list = []

    load_dotenv()
    apilayer_token = os.getenv("APILAYER_TOKEN")
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": apilayer_token}

    for currency_code in user_currencies_list:

        payload = {"amount": 1, "from": currency_code, "to": "RUB"}

        if "test" in user_currencies_list:
            response_dict = {
                "success": True,
                "query": {"from": "GBP", "to": "RUB", "amount": 1},
                "info": {"timestamp": 1724153824, "rate": 119.262948},
                "date": "2024-08-20",
                "result": 119.262948,
            }
        else:
            response = requests.get(url, headers=headers, params=payload)
            response_dict = response.json()

        rates_dicts_list.append({"currency": currency_code, "rate": round(response_dict["info"]["rate"], 2)})
    # print("response.status_code: ", response.status_code)
    #     print("response.json(): ", response.json())
    # response.status_code: 200
    # response.json(): {'success': True,
    #                   'query': {'from': 'GBP', 'to': 'RUB', 'amount': 1},
    #                   'info': {'timestamp': 1724044816, 'rate': 114.535684},
    #                   'date': '2024-08-19',
    #                   'result': 114.535684
    #                   }
    # print(response_dict, "\n")
    return rates_dicts_list


# print(generate_rates_dicts_with_api(["GBP", "EUR", "USD", "JPY"]))


def get_stocks_from_user_file() -> list:
    """Возвращает список акций из user_settings.json файла."""

    # file_path = "../user_settings.json"
    if __name__ == "__main__" or __name__ == "utils":
        file_path = "../user_settings.json"
    else:
        file_path = "./user_settings.json"
    # Если файл не существует:
    if not os.path.exists(file_path):
        raise ValueError("Файл user_settings.json не найден.")

    with open(file_path, "r", encoding="utf-8") as file:
        json_data_dict = json.load(file)

    if type(json_data_dict) is dict and "user_stocks" in json_data_dict:
        if type(json_data_dict["user_stocks"]) is list:
            return json_data_dict["user_stocks"]
    return []


def generate_stocks_dicts_with_api(user_stocks_list: list) -> list[dict]:
    """
    Принимает:  Список с названиями акций.
    Возвращает: Список со словарями вида {"currency": "GBP", "rate": 114.53}
    """
    prices_dicts_list = []

    load_dotenv()
    marketstack_api_key = os.getenv("MARKETSTACK_API_KEY")
    # url = f"https://api.marketstack.com/v1/intraday?access_key={marketstack_api_key}"
    url = f"https://api.marketstack.com/v1/eod?access_key={marketstack_api_key}"

    for stock_code in user_stocks_list:
        if "test" in user_stocks_list:
            response_dict = {
                "pagination": {"limit": 100, "offset": 0, "count": 100, "total": 251},
                "data": [{"open": 225.72, "high": 225.99, "low": 223.04, "close": 225.89}],
            }
        else:
            querystring = {"symbols": stock_code}
            response = requests.get(url, params=querystring)
            response_dict = response.json()
        # print(response_dict)
        # for key, value in response_dict.items():
        #     if key == "data":
        #         for dict_ in response_dict["data"]:
        #             print(dict_)

        prices_dicts_list.append({"stock": stock_code, "price": round(response_dict["data"][0]["close"], 2)})
    # print("response.status_code: ", response.status_code)
    # print("response.json(): ", response.json())
    return prices_dicts_list


# prices_dicts_list = generate_stocks_dicts_with_api(['AAPL', 'AMZN'])
# prices_dicts_list = generate_stocks_dicts_with_api(['AAPL'])
# print(prices_dicts_list)
# [{'stock': 'AAPL', 'price': 226.05}, {'stock': 'AMZN', 'price': 177.06}]
