from src.views import generate_json_for_main_page
from src.utils import read_main_data_from_excel
from src.abs_paths import get_absolute_path_for_file


operations_xlsx_path = get_absolute_path_for_file("operations.xlsx")
main_df = read_main_data_from_excel(operations_xlsx_path)


def test_generate_json_for_main_page___test_return_type():
    json_str = generate_json_for_main_page("2021-10-02 08:34:56", main_df)
    assert type(json_str) is str
