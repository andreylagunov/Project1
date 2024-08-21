import json
import os.path

import pandas as pd

from src.utils import read_main_data_from_excel
from src.utils import get_greeting_by_hours
from src.utils import get_df_by_date
from src.utils import generate_cards_numbers_list
from src.utils import generate_cards_spendings_dict
from src.utils import generate_cards_cashbacks_dict
from src.utils import generate_cards_info_list
from src.utils import generate_top_five_trans_list
from src.utils import write_data_to_user_settings_json
from src.utils import get_currencies_from_user_file
from src.utils import get_stocks_from_user_file
from src.utils import generate_rates_dicts_with_api
from src.utils import generate_stocks_dicts_with_api
from pytest import mark, raises
# from unittest.mock import patch
import datetime

import pandas


def test_read_main_data_from_excel___empty_file():
    with raises(ValueError) as exception_info:
        read_main_data_from_excel("data/empty_test.xlsx")
    assert str(exception_info.value) == "При попытке чтения excel-файла, он содержит некорректные данные"

def test_read_main_data_from_excel___check_type():
    assert type(read_main_data_from_excel("data/operations.xlsx")) == pandas.DataFrame

def test_read_main_data_from_excel___check_data():
    df = read_main_data_from_excel("data/operations.xlsx")
    assert df["Категория"][0] == "Супермаркеты"
    assert df["Категория"][4] == "Различные товары"

def test_get_greeting_by_hours___normal():
    assert get_greeting_by_hours(5) == "Доброй ночи"
    assert get_greeting_by_hours(12) == "Доброе утро"
    assert get_greeting_by_hours(14) == "Добрый день"
    assert get_greeting_by_hours(23) == "Добрый вечер"

def test_get_greeting_by_hours___with_not_int_type():
    with raises(ValueError) as exception_info:
        # Передаётся не тип int
        get_greeting_by_hours(9.9)
    assert str(exception_info.value) == "Ожидался тип int."

def test_get_greeting_by_hours___hour_without_range():
    with raises(ValueError) as exception_info:
        # Передаётся некорректный час
        get_greeting_by_hours(-35)
    assert str(exception_info.value) == "Время (час) ожидалось в диапазоне 0-24 включительно."


def test_get_df_by_date():
    main_df = read_main_data_from_excel("data/operations.xlsx")
    # Создание объекта datetime:
    datetime_obj = datetime.datetime.strptime("2021-08-21 04:30:34", "%Y-%m-%d %H:%M:%S")
    # Фильтрация входящего датафрейма по текущему месяцу:
    df_by_date = get_df_by_date(main_df, datetime_obj)
    assert type(df_by_date) is pd.DataFrame


def test_generate_cards_numbers_list():
    main_df = read_main_data_from_excel("data/operations.xlsx")
    cards = generate_cards_numbers_list(main_df)
    for number in cards:
        assert type(number) is str
        assert len(number) == len("*0000")


def test_generate_cards_spendings_dict():
    main_df = read_main_data_from_excel("data/operations.xlsx")
    # Создание объекта datetime:
    datetime_obj = datetime.datetime.strptime("2021-08-21 04:30:34", "%Y-%m-%d %H:%M:%S")
    # Фильтрация входящего датафрейма по текущему месяцу:
    df_by_date = get_df_by_date(main_df, datetime_obj)
    dict_ = generate_cards_spendings_dict(['*7197', '*6002', '*4556', '*5441'], df_by_date)
    for card, spending in dict_.items():
        assert type(spending) in (float, int)


def test_generate_cards_cashbacks_dict():
    spendings_dict = {'*7197': 7236.32, '*4556': 500}
    assert generate_cards_cashbacks_dict(spendings_dict) == {
        '*7197': 72.36,
        '*4556': 5.00
    }


def test_generate_cards_info_list():
    spendings_dict = {'*4556': 500}
    cashbacks_dict = {'*4556': 5.00}
    assert generate_cards_info_list(spendings_dict, cashbacks_dict) == [{
            "last_digits": "4556",
            "total_spent": 500,
            "cashback": 5.00
        }]


def test_generate_top_five_trans_list():
    main_df = read_main_data_from_excel("data/operations.xlsx")
    # Создание объекта datetime:
    datetime_obj = datetime.datetime.strptime("2021-08-21 04:30:34", "%Y-%m-%d %H:%M:%S")
    # Фильтрация входящего датафрейма по текущему месяцу:
    df_by_date = get_df_by_date(main_df, datetime_obj)
    top_five_trans_list = generate_top_five_trans_list(df_by_date)
    assert type(top_five_trans_list) is list
    assert len(top_five_trans_list) == 5
    for trans_dict in top_five_trans_list:
        assert type(trans_dict) is dict
        assert "date" in trans_dict
        assert "amount" in trans_dict
        assert "category" in trans_dict
        assert "description" in trans_dict
        # {'date': '01.10.2021', 'amount': -492.0, 'category': 'Дом и ремонт', 'description': 'МаксидоМ'},


def test_write_data_to_user_settings_json():
    # if os.path.exists("./user_settings.json"):
    #     os.truncate("./user_settings.json", 0)

    write_data_to_user_settings_json({3: [1, 2, 3]})
    assert os.path.exists("./user_settings.json")

    with open("./user_settings.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data == {"3": [1, 2, 3]}
    assert type(data) is dict


def test_get_currencies_from_user_file():
    # Запись данных о валютах и акциях в json-файл:
    currencies_and_stocks_dict = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    write_data_to_user_settings_json(currencies_and_stocks_dict)

    user_currencies_list = get_currencies_from_user_file()
    # ['USD', 'EUR']
    assert user_currencies_list == ['USD', 'EUR']


def test_get_stocks_from_user_file():
    # Запись данных о валютах и акциях в json-файл:
    currencies_and_stocks_dict = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    write_data_to_user_settings_json(currencies_and_stocks_dict)

    user_stocks_list = get_stocks_from_user_file()
    # ["AAPL", "AMZN"]
    assert user_stocks_list == ["AAPL", "AMZN"]


def test_generate_rates_dicts_with_api():
    currencies_rates_list = generate_rates_dicts_with_api(['test'])
    # [{'currency': 'USD', 'rate': 89.0}, {'currency': 'EUR', 'rate': 98.35}]
    assert currencies_rates_list == [{'currency': 'test', 'rate': 119.26}]


def test_generate_stocks_dicts_with_api():
    stocks_prices_list = generate_stocks_dicts_with_api(['test'])
    # [{'stock': 'AAPL', 'price': 226.05}, {'stock': 'AMZN', 'price': 177.06}]
    assert stocks_prices_list == [{'stock': 'test', 'price': 225.89}]
