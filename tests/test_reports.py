from src.reports import spending_by_category
from src.reports import decorator_for_json_write
from src.reports import decorator_for_json_write___in_file
from src.utils import read_main_data_from_excel
from pytest import mark, raises
import pandas as pd
import os


def test_spending_by_category___test_categories():
    df = read_main_data_from_excel("data/operations.xlsx")
    filtered_df = spending_by_category(df, "Аптеки", "28.08.2020")
    for index, row in filtered_df.iterrows():
        assert row["Категория"] == "Аптеки"

    filtered_df = spending_by_category(df, "Супермаркеты", "28.08.2020")
    for index, row in filtered_df.iterrows():
        assert row["Категория"] == "Супермаркеты"

# by_category = decorator_for_json_write(spending_by_category)
# df = read_main_data_from_excel("../data/operations.xlsx")
# filtered_df = spending_by_category(df, "Аптеки", "28.08.2020")
# # print(filtered_df)


def test_spending_by_category___test_return_type():
    df = read_main_data_from_excel("data/operations.xlsx")
    filtered_df = spending_by_category(df, "Аптеки", "28.08.2020")
    assert type(filtered_df) is pd.DataFrame


def test_spending_by_category___faulty_dataframe():
    with raises(ValueError) as exception_info:
        # Вместо pd.DataFrame передаётся int.
        spending_by_category(10, "Аптеки", "28.08.2020")
    assert str(exception_info.value) == "Параметр transactions - не типа pandas.DataFrame"


def test_spending_by_category___faulty_date():
    with raises(ValueError) as exception_info:
        df = read_main_data_from_excel("data/operations.xlsx")
        # Передается некорректный тип даты.
        spending_by_category(df, "Аптеки", 234)
    assert str(exception_info.value) == "Параметр date - не типа str"


def test_spending_by_category___faulty_category():
    with raises(ValueError) as exception_info:
        df = read_main_data_from_excel("data/operations.xlsx")
        # Передается некорректный тип категории.
        spending_by_category(df, 4.5, "28.08.2020")
    assert str(exception_info.value) == "Параметр category - не типа str"


def test_decorator_for_json_write():
    # Удаляем файл data/spendings_report.json
    json_file_path = "data/spendings_report.json"
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    assert os.path.exists(json_file_path) == False

    # spending_by_category = decorator_for_json_write(spending_by_category)
    spending_by_category_decor = decorator_for_json_write(spending_by_category)
    df = read_main_data_from_excel("data/operations.xlsx")
    filtered_df = spending_by_category_decor(df, "Аптеки", "28.08.2020")
    assert type(filtered_df) is pd.DataFrame
    assert os.path.exists(json_file_path) == True


def test_decorator_for_json_write___in_file():
    # Удаляем файл data/report_file.json
    json_file_path = "data/report_file.json"
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    assert os.path.exists(json_file_path) == False

    spending_by_category___wrapper = decorator_for_json_write___in_file(json_file_path)
    spending_by_category___inner = spending_by_category___wrapper(spending_by_category)
    df = read_main_data_from_excel("data/operations.xlsx")
    filtered_df = spending_by_category___inner(df, "Аптеки", "28.08.2020")
    assert type(filtered_df) is pd.DataFrame
    assert os.path.exists(json_file_path) == True
