from src.services import investment_bank
from pytest import mark, raises


def test_investment_bank___faulty_month(get_operations_list___normal___for_investment_bank):
    with raises(ValueError) as exception_info:
        # Передаётся month-строка не соответствующей длины.
        investment_bank("2021.03.", get_operations_list___normal___for_investment_bank, 100)
    assert str(exception_info.value) == "Параметр month: ожидалась строка вида 'YYYY.MM'"


def test_investment_bank___trans_data_is_not_list(get_not_operations_list___for_investment_bank):
    with raises(ValueError) as exception_info:
        # Вместо списка данных передаётся другой тип.
        investment_bank("2021.03", get_not_operations_list___for_investment_bank, 100)
    assert str(exception_info.value) == "Параметр transactions: должен быть типа list (непустым)"


def test_investment_bank___trans_data_is_empty_list(get_empty_operations_list___for_investment_bank):
    with raises(ValueError) as exception_info:
        # В списке транзакций ничего нет.
        investment_bank("2021.03", get_empty_operations_list___for_investment_bank, 100)
    assert str(exception_info.value) == "Параметр transactions: должен быть типа list (непустым)"


def test_investment_bank___trans_data_with_faulty_dict(get_faulty_operations_list___for_investment_bank):
    with raises(ValueError) as exception_info:
        # В списке транзакций есть элементы - не словари.
        investment_bank("2021.03", get_faulty_operations_list___for_investment_bank, 100)
    assert str(exception_info.value) == "Элемент списка транзакций - не словарь"


def test_investment_bank___faulty_limit(get_operations_list___normal___for_investment_bank):
    assert investment_bank("2021.03", get_operations_list___normal___for_investment_bank, "100") != None


def test_investment_bank___normal(get_operations_list___normal___for_investment_bank):
    assert investment_bank("2021.03", get_operations_list___normal___for_investment_bank, 10) == "14.5"


def test_investment_bank___faulty_sums(get_operations_list___faulty_sum___for_investment_bank):
    assert investment_bank("2021.03", get_operations_list___faulty_sum___for_investment_bank, 10) == "14.5"
