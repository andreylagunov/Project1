import os
# import pprint


def create_absulute_paths() -> dict:
    """
    Вспомогательная функция. Генерирует абсолютные пути к файлам логов и данным.
    Возвращает словарь вида {"file_name": "absolute_file_path"}
    """
    directory = os.getcwd().split("/")[-1]
    # print("directory: ", directory)
    if directory == "Project_1":
        insertion = ""
    elif directory == "src":
        insertion = "../"
    else:
        raise ValueError("При генерировании абсолютных путей: ошибка с именем текущего каталога.")
    # print("Выбрали insertion: ", insertion)
    paths = {
        "reports.log": os.path.abspath(f"{insertion}logs/reports.log"),
        "services.log": os.path.abspath(f"{insertion}logs/services.log"),
        "utils.log": os.path.abspath(f"{insertion}logs/utils.log"),
        "operations.xlsx": os.path.abspath(f"{insertion}data/operations.xlsx"),
        "empty_test.xlsx": os.path.abspath(f"{insertion}data/empty_test.xlsx"),
        "report_file.json": os.path.abspath(f"{insertion}data/report_file.json"),
        "spendings_report.json": os.path.abspath(f"{insertion}data/spendings_report.json"),
        "test_for_write.json": os.path.abspath(f"{insertion}data/test_for_write.json"),
        "user_settings.json": os.path.abspath(f"{insertion}user_settings.json")
    }
    return paths


absulute_paths_dict = create_absulute_paths()
# pprint.pprint(absulute_paths_dict)


def get_absolute_path_for_file(file_name: str) -> str:
    """
    :param file_name:   Имя файла, для которого необходимо вернуть аболютный путь.
    :return:            Абсолютный путь,
                        который был сгененрирован функцией create_absolute_paths()
    """
    return str(absulute_paths_dict.get(file_name))
