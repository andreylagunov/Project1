import datetime
import json
import logging
import os
from typing import Any, Dict, List

if __name__ == "__main__":
    log_file_path = "../logs/services.log"
else:
    log_file_path = "logs/services.log"

if os.path.exists(log_file_path):
    os.truncate(log_file_path, 0)

logger = logging.getLogger("investment_bank")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s   %(name)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """
    :param month:           месяц ("YYYY.MM"), для которого рассчитывается отложенная сумма
    :param transactions:    список словарей вида {"YYYY.MM.DD": сумма операции(число)}
    :param limit:           предел округления для сумм операций (целое число)
    :return:                сумма, которую удалось бы отложить
    """
    sum = 0
    if type(month) is not str or len(month) != len("YYYY.MM"):
        logger.error("Параметр month: ожидалась строка вида 'YYYY.MM'")
        raise ValueError("Параметр month: ожидалась строка вида 'YYYY.MM'")

    if type(transactions) is not list or len(transactions) == 0:
        logger.error("Параметр transactions: должен быть типа list (непустым)")
        raise ValueError("Параметр transactions: должен быть типа list (непустым)")

    required_date_obj = datetime.datetime.strptime(month, "%Y.%m")
    logger.debug(f"Переданная дата в функцию: {required_date_obj.year}.{required_date_obj.month}")

    # Если передан limit не из числа стандартных сумм округления,
    # установка limit в значение - 10 руб.
    if limit not in (10, 50, 100):
        limit = 10
        logger.warning("Параметр limit: не в числе стандартных сумм округления.")
        logger.info("Установка limit в значение - 10 руб.")

    for dict_ in transactions:
        if type(dict_) is not dict:
            logger.error("Элемент списка транзакций - не словарь")
            raise ValueError("Элемент списка транзакций - не словарь")

        if type(dict_["Дата операции"]) is not str or len(dict_["Дата операции"]) != len("YYYY.MM.DD"):
            logger.warning("Значение в столбце 'Дата операции': ожидалась строка вида 'YYYY.MM.DD'")
            continue
        date_obj = datetime.datetime.strptime(dict_["Дата операции"], "%Y.%m.%d")

        if (
            date_obj.year == required_date_obj.year
            and date_obj.month == required_date_obj.month
            and (type(dict_["Сумма операции"]) is float or type(dict_["Сумма операции"]) is int)
            and dict_["Сумма операции"] < 0
        ):

            abs_sum = abs(dict_["Сумма операции"])
            remainder = abs_sum % limit
            logger.info(f"Для суммы {abs_sum} остаток от деления на {limit} равен {round(remainder, 2)}")
            if remainder:
                sum_to_investment_from_trans = limit - remainder
                logger.info(f"Откладываем в копилку {round(sum_to_investment_from_trans, 2)}\n")
                # print(f"Откладываем в копилку {round(sum_to_investment_from_trans, 2)}\n")
                sum += sum_to_investment_from_trans

    # return round(sum, 2)
    json_result = json.dumps(sum)
    logger.debug(f"Возвращаемое значение: {json_result}, тип: {type(json_result)}")
    return json_result


# operations_list = [
#     {"Дата операции": "2021.03.24", "Сумма операции": -17980.0},
#     {"Дата операции": "2021.03.27", "Сумма операции": -534.50},
#     {"Дата операции": "2021.03.30", "Сумма операции": -2401.0},
#     {"Дата операции": "2021.04.01", "Сумма операции": 750.0},
#     {"Дата операции": "2021.04.01", "Сумма операции": 123.0},
#     {"Дата операции": "2021.04.04", "Сумма операции": 2105.6},
#     {"Дата операции": "2021.04.06", "Сумма операции": 56.6},
#     {"Дата операции": "2021.04.07", "Сумма операции": 987.5},
#     {"Дата операции": "2021.05.01", "Сумма операции": 3459.5},
#     {"Дата операции": "2021.05.02", "Сумма операции": 146.0},
#     {"Дата операции": "2021.05.03", "Сумма операции": 977.0},
# ]
#
#
# json_sum = investment_bank("2021.03", operations_list, 10)
# print(json_sum, type(json_sum))
