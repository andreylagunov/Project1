import datetime
import json
import logging
import os
from functools import wraps
from typing import Callable, Optional

import pandas as pd

# from src.utils import read_main_data_from_excel

if __name__ == "__main__":
    report_file___default_path = "../data/spendings_report.json"
    log_file_path = "../logs/reports.log"
else:
    report_file___default_path = "data/spendings_report.json"
    log_file_path = "logs/reports.log"

if os.path.exists(log_file_path):
    os.truncate(log_file_path, 0)

logger = logging.getLogger("reports.py")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s   %(name)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def decorator_for_json_write(func: Callable) -> Callable:
    """
    Принимает:  функцию, которую необходимо обернуть.
    Возвращает: обёрнутую в функциональность,
    дополнительно записывающую json-файл (файл по умолчанию).
    """

    @wraps(func)
    def wrapper(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """
        Функция-обёртка над func-функцией.
        Принимает: Параметры для основной функции.
        Дополнительно производит запись данных в json-файл.
        Возвращает: Данные основной функции в неизменном виде.
        """
        logger.debug("=" * 80)
        logger.debug(f"Выполнение функции {func.__name__} в обёртке:")

        df_ = func(transactions, category, date)
        if type(df_) is pd.DataFrame:
            logger.debug("Обёрнутая функция вернула тип pandas.DataFrame - OK")
        else:
            logger.debug("Обёрнутая функция вернула НЕ тип pandas.DataFrame - Остановка выполнения")
            raise ValueError("Обёрнутая функция вернула НЕ тип pandas.DataFrame - Остановка выполнения")
        # Преобразование типа DataFrame в тип, работающий с json-библиотекой:
        # Каждая строка датафрейма преобразуется в список словарей,
        # где ключ - имя столбца, а значение - значение с данной строке/столбце.
        columns_list = list(df_.keys())
        summary_list = []

        for index, row in df_.iterrows():
            row_list = []
            for column_name in columns_list:
                row_list.append({column_name: row[column_name]})
            summary_list.append(row_list)

        # for list_ in summary_list:
        #     print(list_)

        with open(report_file___default_path, "w", encoding="utf-8") as file:
            json.dump(summary_list, file, ensure_ascii=False)
        logger.debug(f"Запись json-файла по пути {report_file___default_path} прошла успешно")
        logger.debug(f"Нормальное завершение обёрнутой функции {func.__name__}")
        return pd.DataFrame(df_)

    return wrapper


def decorator_for_json_write___in_file(file_path: str) -> Callable:
    """
    Принимает:  Путь до файла, в который будет происходить запись json-формата.
    Возвращает: Внутреннюю wrapper функцию.
    """

    def wrapper(func: Callable) -> Callable:
        """
        Принимает:  Функцию func, которую необходимо обернуть.
        Возвращает: Функцию-обёртку inner над func-функцией.
        """

        @wraps(func)
        def inner(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
            """
            Принимает:  Аргументы для основной функции func.
            Возвращает: Результат работы основной функции func - фильтрованный датафрейм.
            Обёртка дополнительно создаёт json-файл с данными датафрейма, записывая данные
            в файл по пути, указанном пользователем.
            """
            logger.debug("=" * 80)
            logger.debug(f"Выполнение функции {func.__name__} в обёртке:")

            df_ = func(transactions, category, date)
            if type(df_) is pd.DataFrame:
                logger.debug("Обёрнутая функция вернула тип pandas.DataFrame - OK")
            else:
                logger.debug("Обёрнутая функция вернула НЕ тип pandas.DataFrame - Остановка выполнения")
                raise ValueError("Обёрнутая функция вернула НЕ тип pandas.DataFrame - Остановка выполнения")
            # Преобразование типа DataFrame в тип, работающий с json-библиотекой:
            # Каждая строка датафрейма преобразуется в список словарей,
            # где ключ - имя столбца, а значение - значение с данной строке/столбце.
            columns_list = list(df_.keys())
            summary_list = []

            for index, row in df_.iterrows():
                row_list = []
                for column_name in columns_list:
                    row_list.append({column_name: row[column_name]})
                summary_list.append(row_list)

            # for list_ in summary_list:
            #     print(list_)

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(summary_list, file, ensure_ascii=False)
            logger.debug(f"Запись json-файла по пути {report_file___default_path} прошла успешно")
            logger.debug(f"Нормальное завершение обёрнутой функции {func.__name__}")
            return pd.DataFrame(df_)

        return inner

    return wrapper


# @decorator_for_json_write
# @decorator_for_json_write___in_file("../data/report_file.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает:  Датафрейм транзакций, название категории, опционально - дату вида "dd.mm.yyyy".
    Если дата не передана - берётся текущая дата.
    Возвращает: Датафрейм с тратами за последние 3 месяца от переданной/текущей даты.
    """
    logger.debug("=" * 80)
    logger.debug("Выполнение функции spending_by_category:")
    if type(transactions) is not pd.DataFrame:
        logger.error("Параметр transactions - не типа pandas.DataFrame")
        raise ValueError("Параметр transactions - не типа pandas.DataFrame")

    if type(category) is not str:
        logger.error("Параметр category - не типа str")
        raise ValueError("Параметр category - не типа str")

    if type(date) is not str and type(date) is not None:
        logger.error("Параметр date - не типа str")
        raise ValueError("Параметр date - не типа str")

    # Создание объекта datetime:
    if type(date) is str and len(date) == len("dd.mm.yyyy"):
        datetime_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    else:
        datetime_obj = datetime.datetime.now()
    # print(datetime_obj.year)
    end_day = datetime_obj.day
    end_month = datetime_obj.month
    end_year = datetime_obj.year

    # Расчёт даты от переданной/текущей, от которой (since) необходимо вывести информацию.
    # День остаётся неизменным. Изменяться будет месяц, год в том числе.
    since_day = datetime_obj.day
    since_year = datetime_obj.year
    if datetime_obj.month > 3:
        since_month = datetime_obj.month - 3
    elif datetime_obj.month == 3:
        since_month = 12
        since_year -= 1
    else:
        since_month = 12 - (3 - datetime_obj.month)
        since_year -= 1
    # print(datetime_obj.day, datetime_obj.month, datetime_obj.year)
    # print(since_day, since_month, since_year)
    logger.debug(f"Фильтрация    с даты: {since_day}.{since_month}.{since_year}")
    logger.debug(f"             по дату: {end_day}.{end_month}.{end_year}")

    # Создание float-эквивалентных дат:
    since_float = since_year + ((since_month - 1) / 12) + since_day / 365
    end_float = end_year + ((end_month - 1) / 12) + end_day / 365
    logger.debug("Даты, приведённые к float-значениям:")
    logger.debug(f"              с даты: {round(since_float, 2)}")
    logger.debug(f"             по дату: {round(end_float, 2)}")

    # Инициализация нового датафрейма с такими же столбцами:
    df_by_last_three_months = pd.DataFrame(columns=list(transactions.keys()))

    # Фильтрация датафрейма по вхождению в диапазон трёх месяцев:
    for index, row in transactions.iterrows():
        # Создание объекта datetime из Даты операции:
        row_datetime_obj = datetime.datetime.strptime(str(row["Дата операции"]), "%d.%m.%Y %H:%M:%S")

        # Создание float-эквивалентной даты:
        row_date_float = row_datetime_obj.year + ((row_datetime_obj.month - 1) / 12) + row_datetime_obj.day / 365

        if since_float <= row_date_float <= end_float:
            if type(row["Категория"]) is str and row["Категория"] == category:
                # df_by_date.loc[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                if type(index) is int:
                    df_by_last_three_months.loc[index] = list(dict(row).values())

    logger.debug("Нормальное завершение функции spending_by_category")
    return df_by_last_three_months


# spending_by_category = decorator_for_json_write(spending_by_category)

# df = read_main_data_from_excel("../data/operations.xlsx")
# filtered_df = spending_by_category(df, "Аптеки", "28.08.2020")
# print(filtered_df)
