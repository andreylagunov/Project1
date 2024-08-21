# Виджет банковских операций клиента.


## Описание:

Учебный проект


## Необходимое ПО:

1. PyCharm IDE (или другая)
2. poetry
3. git
4. pytest
5. pytest-cov


## Для тестирования функций:

1. Клонируйте репозиторий:
```
git@github.com:andreylagunov/Project_1.git
```

2. Установите зависимости:

```
poetry install 
```

3. Для запуска тестирования инструментом pytest:

```
pytest
```

4. Для формирования отчёта о покрытии тестами инструментом pytest-cov:

```
pytest --cov=src --cov-report=html
```


## Описание работы функций:


### Модуль **main.py**
Позволяет проверить работы трёх основных функций:
```
# Генерация ответа json-формата Главной странице.
json_str = generate_json_for_main_page("2021-10-02 08:34:56", dataframe)
   
# Фильтрация по категории за последние три месяца.
dataframe_2 = spending_by_category(dataframe_1, "Транспорт", "28.08.2020")

# Рассчёт возможной суммы в "Инвесткопилку", задавая сумму для округления.
json_sum = investment_bank("2021.05", operations_list, 10)
```


### Модуль **services.py**
Реализует функцию "Инвесткопилки"
```
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """
    :param month:           месяц ("YYYY.MM"), для которого рассчитывается отложенная сумма
    :param transactions:    список словарей вида {"YYYY.MM.DD": сумма операции(число)}
    :param limit:           предел округления для сумм операций (целое число)
    :return:                сумма, которую удалось бы отложить
    """
```


### Модуль **views.py**
Реализует функцию генерации ответа странице "Главная"
```
def generate_json_for_main_page(date_and_time_str: str, df: pd.DataFrame) -> str:
    """
    Принимает:  строку с датой и временем формата "YYYY-MM-DD HH:MM:SS"
    Возвращает: JSON-ответ главной странице.
    """
```


### Модуль **utils.py**
Реализует функции, на которых основан ответ странице "Главная"
```
def read_main_data_from_excel(file_path: str) -> pd.DataFrame:
    """
    Принимает путь до excel файла.
    Возвращает объект DataFrame с содержимым файла.
    """
    
def get_greeting_by_hours(hour: int) -> str:
    """
    Принимает текущее время (час).
    Возвращает строку приветствия: "Доброй ночи / Доброе утро / Добрый день / Добрый вечер"
    """
    
def get_df_by_date(df: pd.DataFrame, datetime_obj: datetime.datetime) -> pd.DataFrame | None:
    """
    Принимает:  Датафрейм и объект даты/времени.
    Возвращает: новый Датафрейм,
                отфильтрованный по дате в диапазоне: Начало месяца - Входящая дата
    """
    
def generate_cards_numbers_list(df: pd.DataFrame) -> list:
    """
    Принимает:  Датафрейм.
    Возвращает: Список номер карт, содержащихся в датафрейме.
    """
    
def generate_cards_spendings_dict(cards_numbers_list: list, df_by_date: pd.DataFrame) -> dict:
    """
    Принимает:  Список номеров карт.
    Возвращает: Словарь с парами {"Номер карты": "траты в текущем месяце"}
    """
    
def generate_cards_cashbacks_dict(cards_spendings_dict: dict) -> dict:
    """
    Принимает:  Словарь с {картами: тратами}.
    Возвращает: Словарь с {картами: кешбэком}.
    """
    
def generate_cards_info_list(spendings: dict, cashbacks: dict) -> list[dict]:
    """
    Принимает:  Два словаря - с тратами по картам, с кешбэками по картам.
    Возвращает: Список словарей (словарь согласно ТЗ).
    """
    
def generate_top_five_trans_list(df_by_date: pd.DataFrame) -> list[dict[str, Any] | None]:
    """
    Принимает:  Датафрейм по текущему месяцу.
    Возвращает: Список словарей транзакций с максимальными суммами операций.
    """
    
def write_data_to_user_settings_json(data_dict: dict) -> None:
    """
    Принимает:  Словарь с данными по акциям и валютам.
    Записывает данные в user_settings.json файл.
    """
    
def get_currencies_from_user_file() -> list:
    """Возвращает список с валютами из user_settings.json файла."""
    
def generate_rates_dicts_with_api(user_currencies_list: list) -> list[dict]:
    """
    Принимает:  Список с валютами.
    Возвращает: Список со словарями вида {"currency": "GBP", "rate": 114.53}
    """
    
def get_stocks_from_user_file() -> list:
    """Возвращает список акций из user_settings.json файла."""
    
def generate_stocks_dicts_with_api(user_stocks_list: list) -> list[dict]:
    """
    Принимает:  Список с названиями акций.
    Возвращает: Список со словарями вида {"currency": "GBP", "rate": 114.53}
    """
```


### Модуль **reports.py**
Реализует функцию отчёта "Траты по категории"
```
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает:  Датафрейм транзакций, название категории, опционально - дату вида "dd.mm.yyyy".
    Если дата не передана - берётся текущая дата.
    Возвращает: Датафрейм с тратами за последние 3 месяца от переданной/текущей даты.
    """
    
def decorator_for_json_write(func: Callable) -> Callable:
    """
    Принимает:  функцию, которую необходимо обернуть.
    Возвращает: обёрнутую в функциональность,
    дополнительно записывающую json-файл (файл по умолчанию).
    """
    
def decorator_for_json_write___in_file(file_path: str) -> Callable:
    """
    Принимает:  Путь до файла, в который будет происходить запись json-формата.
    Возвращает: Внутреннюю wrapper функцию.
    """
```


### Модуль **abs_paths.py**
Вспомогательная функциональность контроля путей к файлам.
```
def create_absulute_paths() -> dict:
    """
    Вспомогательная функция. Генерирует абсолютные пути к файлам логов и данным.
    Возвращает словарь вида {"file_name": "absolute_file_path"}
    """
    
def get_absolute_path_for_file(file_name: str) -> str:
    """
    :param file_name:   Имя файла, для которого необходимо вернуть аболютный путь.
    :return:            Абсолютный путь,
                        который был сгененрирован функцией create_absolute_paths()
    """
```



## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).