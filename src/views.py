import datetime
import json

import pandas as pd

# from utils import write_data_to_user_settings_json
from src.utils import read_main_data_from_excel
# import os
from src.utils import (generate_cards_cashbacks_dict, generate_cards_info_list, generate_cards_numbers_list,
                   generate_cards_spendings_dict, generate_rates_dicts_with_api, generate_stocks_dicts_with_api,
                   generate_top_five_trans_list, get_currencies_from_user_file, get_df_by_date, get_greeting_by_hours,
                   get_stocks_from_user_file)


def generate_json_for_main_page(date_and_time_str: str, df: pd.DataFrame) -> str:
    """
    Принимает:  строку с датой и временем формата "YYYY-MM-DD HH:MM:SS"
    Возвращает: JSON-ответ главной странице.
    """
    json_answer = dict()

    # Создание объекта datetime:
    datetime_obj = datetime.datetime.strptime(date_and_time_str, "%Y-%m-%d %H:%M:%S")

    # Фильтрация входящего датафрейма по текущему месяцу:
    df_by_date = get_df_by_date(df, datetime_obj)
    # =============================================================================================
    # =========================        ФОРМИРОВАНИЕ ПРИВЕТСТВИЯ        ============================
    # =============================================================================================

    greeting = get_greeting_by_hours(datetime_obj.hour)

    # Добавление в JSON-ответ пары по ключу "greeting":
    json_answer["greeting"] = greeting

    # ============================================================================================
    # ============      ФОРМИРОВАНИЕ СПИСКА СЛОВАРЕЙ:   КАРТЫ, ТРАТЫ, КЕШБЭК        ==============
    # ============================================================================================

    cards_numbers_list = generate_cards_numbers_list(df)
    # ['*5091', '*5507', '*7197', '*6002', '*4556', '*1112', '*5441']

    # Формирование для списка карт суммы расходов по каждой:
    cards_spendings_dict = generate_cards_spendings_dict(cards_numbers_list, df_by_date)
    # {'*1112': 0, '*5441': 0, '*5091': 0, '*7197': 7236.32, '*4556': 0, '*5507': 0, '*6002': 0}

    # Формирование словаря с кешбэками по картам:
    cards_cashbacks_dict = generate_cards_cashbacks_dict(cards_spendings_dict)
    # {'*5441': 0.0, '*6002': 0.0, '*5507': 0.0, '*4556': 0.0, '*1112': 0.0, '*5091': 0.0, '*7197': 72.36}

    # Формирование списка словарей для карт:
    cards_info_list = generate_cards_info_list(cards_spendings_dict, cards_cashbacks_dict)
    # [{'last_digits': '6002', 'total_spent': 0, 'cashback': 0.0},
    # {'last_digits': '7197', 'total_spent': 7236.32, 'cashback': 72.36},
    # ...
    # {'last_digits': '5441', 'total_spent': 0, 'cashback': 0.0}]

    # Добавление в JSON-ответ пары по ключу "cards":
    json_answer["cards"] = cards_info_list

    # ============================================================================================
    # ============      ФОРМИРОВАНИЕ СПИСКА TOP-5 ТРАНЗАКЦИЙ ПО СУММЕ ПЛАТЕЖА        =============
    # ============================================================================================

    top_five_trans_list = generate_top_five_trans_list(df_by_date)
    # [{'date': '02.10.2021', 'amount': -5750.4, 'category': 'Каршеринг', 'description': 'Ситидрайв'},
    # {'date': '01.10.2021', 'amount': -581.8, 'category': 'Фастфуд', 'description': 'Пироговый Дворик'},
    # {'date': '01.10.2021', 'amount': -492.0, 'category': 'Дом и ремонт', 'description': 'МаксидоМ'},
    # {'date': '01.10.2021', 'amount': -96.78, 'category': 'Супермаркеты', 'description': 'Колхоз'},
    # {'date': '02.10.2021', 'amount': -93.0, 'category': 'Ж/д билеты', 'description': 'st. Pavlovsk'}]

    # Добавление в JSON-ответ пары по ключу "top_transactions":
    json_answer["top_transactions"] = top_five_trans_list

    # ============================================================================================
    # =======================      ФОРМИРОВАНИЕ СПИСКА КУРСОВ ВАЛЮТ       ========================
    # ============================================================================================

    # Запись данных о валютах и акциях в json-файл:
    # currencies_and_stocks_dict = {
    #     "user_currencies": ["USD", "EUR"],
    #     "user_stocks": ["AAPL", "AMZN"]
    # }
    # write_data_to_user_settings_json(currencies_and_stocks_dict)

    user_currencies_list = get_currencies_from_user_file()
    # ['USD', 'EUR']

    currencies_rates_list = generate_rates_dicts_with_api(user_currencies_list)
    # [{'currency': 'USD', 'rate': 89.0}, {'currency': 'EUR', 'rate': 98.35}]

    # Добавление в JSON-ответ пары по ключу "currency_rates":
    json_answer["currency_rates"] = currencies_rates_list

    # ============================================================================================
    # ========================      ФОРМИРОВАНИЕ СПИСКА ЦЕН АКЦИЙ       ==========================
    # ============================================================================================

    user_stocks_list = get_stocks_from_user_file()
    # ['AAPL', 'AMZN']

    stocks_prices_list = generate_stocks_dicts_with_api(user_stocks_list)
    # [{'stock': 'AAPL', 'price': 226.05}, {'stock': 'AMZN', 'price': 177.06}]

    # Добавление в JSON-ответ пары по ключу "stock_prices":
    json_answer["stock_prices"] = stocks_prices_list

    # print(json_answer)
    # for key, value in json_answer.items():
    #     print(key)
    #     print(value, "\n")
    return json.dumps(json_answer, ensure_ascii=False)


# main_df = read_main_data_from_excel("../data/operations.xlsx")
# json_str = generate_json_for_main_page("2021-10-02 08:34:56", main_df)
# print("json_str: \n", json_str)


# with open("../data/test_for_write.json", "w", encoding="utf-8") as file:
# string = json.dumps(["ff", 55])
# print(type(string))
# print(string, "\n")
# initial_obj = json.loads(string)
# print(type(initial_obj))
# print(initial_obj)
