import pprint

from src.abs_paths import get_absolute_path_for_file
from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import read_main_data_from_excel
from src.views import generate_json_for_main_page

operations_xlsx_path = get_absolute_path_for_file("operations.xlsx")

main_df = read_main_data_from_excel(operations_xlsx_path)
json_str = generate_json_for_main_page("2021-10-02 08:34:56", main_df)
# print("Ответ главной странице: \n", json_str)
print("Ответ главной странице: ")
pprint.pprint(json_str)
print("=" * 100)


filtered_df = spending_by_category(main_df, "Транспорт", "28.08.2020")
print(filtered_df)
print("=" * 100)

operations_list = [
    {"Дата операции": "2021.03.24", "Сумма операции": -17980.0},
    {"Дата операции": "2021.03.27", "Сумма операции": -534.50},
    {"Дата операции": "2021.03.30", "Сумма операции": -2401.0},
    {"Дата операции": "2021.04.01", "Сумма операции": 750.0},
    {"Дата операции": "2021.04.01", "Сумма операции": 123.0},
    {"Дата операции": "2021.04.04", "Сумма операции": 2105.6},
    {"Дата операции": "2021.04.06", "Сумма операции": 56.6},
    {"Дата операции": "2021.04.07", "Сумма операции": 987.5},
    {"Дата операции": "2021.05.01", "Сумма операции": -3459.5},
    {"Дата операции": "2021.05.02", "Сумма операции": -146.0},
    {"Дата операции": "2021.05.03", "Сумма операции": -977.0},
]
json_sum = investment_bank("2021.05", operations_list, 10)
# print(json_sum, type(json_sum))
print(f"В Инвесткопилку: {json_sum} руб.")
print("=" * 100)
