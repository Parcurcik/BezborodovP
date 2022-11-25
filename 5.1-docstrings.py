import csv
import math
from datetime import datetime
from prettytable import PrettyTable
from typing import *


def prettify_val(val):
    """Вытаскивает и обрезает значение из csv файла

        Args:
             val: значение
    """
    if type(val) == list: val = "\n".join(val)
    val = str(val)
    if len(val) > 100: val = val[:100] + "..."
    return val


def parse_money(amount):
    """Парсит валюту по необходимому образцу

        Args:
            amount: денежная единица из csv файла
    """
    money_arr = []
    seq = list(reversed(list(str(amount))))
    for i in range(len(seq)):
        money_arr.append(seq[i])
        if i % 3 == 2: money_arr.append(" ")
    return "".join(reversed(money_arr)).strip()


def true_false(val):
    """Выводит корректное значение

        Args:
            val: true/false/nan
    """
    if val == math.nan: return "nan"
    if val == "True": return "TRUE"
    if val == "False": return "FALSE"
    try:
        val = int(float(val))
    finally:
        return str(val)


def skills(vac, *args):
    """Парсит скиллы

            Args:
                 vac: выбранная вакансия
                 args: аргументы со значением навыков
        """
    for skill in args[1].split(", "):
        if skill not in vac["key_skills"]:
            return False
    return True


def make_filter(func, *args):
    """Декоратор, который фильтрует значение

                Args:
                     func: первичная функция
                     args: аргументы для фильтрации
            """
    def parameter_func(vac):
        return func(vac, *args)

    return parameter_func


def params(vac, *args):
    """Выбирает параметры

                    Args:
                         vac: выбранная вакансия
                         args: аргументы для параметров
                """
    return to_find[vac[reversed_dict[args[0]]]] == args[1]

def param_filter(vac, *args):
    """Фильтр для параметров

            Args:
                 vac: выбранная вакансия
                 args: аргументы для параметров
                    """
    return vac[reversed_dict[args[0]]] == args[1]

def check_premium(vac, *args):
    """Фильтр для поля "Премиум вакансия"

            Args:
                    vac: выбранная вакансия
                    args: аргументы для премиум поля
                        """
    return yes_no[vac["premium"]] == args[1]

def when_filter(vac, *args):
    """Фильтр для даты

            Args:
                vac: выбранная вакансия
                args: аргументы для даты
                            """
    return datetime.strptime(".".join(vac["published_at"].split("T")[0].split("-")[::-1]), "%d.%m.%Y") == datetime.strptime(args[1], "%d.%m.%Y")

def make_salary(vac, *args):
    """Функция которая создает поле 'Зарплата"

            Args:
                 vac: выбранная вакансия
                 args: аргументы для поля зарплата
                            """
    return int(vac["salary_from"]) <= int(args[1]) <= int(vac["salary_to"])


formatter = {
    "Навыки": skills,
    'Оклад': make_salary,
    "Дата публикации вакансии": when_filter,
    "Опыт работы": params,
    "Премиум-вакансия": check_premium,
    "Идентификатор валюты оклада": params,
    "Название": param_filter,
    "Название региона": param_filter,
    "Компания": param_filter,
    "": lambda *x: True
}

to_find = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "Да": "Без вычета налогов",
    "Нет": "С вычетом налогов",
    "TRUE": "Без вычета налогов",
    "FALSE": "С вычетом налогов",
}

yes_no = {
    "FALSE": "Нет",
    "False": "Нет",
    "Нет": "Нет",
    "TRUE": "Да",
    "True": "Да",
    "Да": "Да"
}

translated_dict = {
    "№": "№",
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary": "Оклад",
    "area_name": "Название региона",
    "published_at_date": "Дата публикации вакансии"
}

reversed_dict = {
    "Название": "name",
    "Описание": "description",
    "Навыки": "key_skills",
    "Опыт работы": "experience_id",
    "Премиум-вакансия": "premium",
    "Компания": "employer_name",
    "Нижняя граница вилки оклада": "salary_from",
    "Верхняя граница вилки оклада": "salary_to",
    "Оклад указан до вычета налогов": "salary_gross",
    "Идентификатор валюты оклада": "salary_currency",
    "Оклад": "salary",
    "Название региона": "area_name",
    "Дата и время публикации вакансии": "published_at",
    "Дата публикации вакансии": "published_at_date"
}

currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

exp = [
    "Нет опыта",
    "От 1 года до 3 лет",
    "От 3 до 6 лет",
    "Более 6 лет"
]

dic_sorters = {
    "": lambda v: True,
    "Название": lambda v: v.name,
    "Описание": lambda v: v.description,
    "Компания": lambda v: v.employer_name,
    "Название региона": lambda v: v.area_name,
    "Опыт работы": lambda v: exp.index(to_find[v.experience_id]),
    "Премиум-вакансия": lambda v: yes_no[v.premium],
    "Оклад": lambda v: (int(v.salary.salary_from) + int(v.salary.salary_to)) / 2 * currency_to_rub[
        v.salary.salary_currency],
    "Навыки": lambda v: len(v.key_skills) if type(v.key_skills) == list else 1,
    "Дата публикации вакансии": lambda v: [datetime.strptime(v.published_at, "%Y-%m-%dT%H:%M:%S%z")]
}


class DataSet:
    """Класс с данными

            Args:
                 file_name: название файла
                            """
    def __init__(self, file_name):
        """Инициализирует объект DataSet

                Args:
                     file_name: название файла
                                """
        self.file_name = file_name
        self.vacancies_objects: List[Vacancy] = []
        self.csv_filter()

    def csv_reader(self):
        """Считывает файл

                       Returns:
                            list: ключ-начение
                                       """
        keys = []
        values = []
        cnt = 1
        with open(self.file_name, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if not keys:
                    keys = ["№"] + row
                else:
                    my_row = row.copy()
                    if all(my_row):
                        values.append([str(cnt)] + [true_false(i) for i in row])
                        cnt += 1
        values = list(filter(lambda x: "nan" not in x, values))
        if not len(keys):
            print("Пустой файл")
            exit(0)
        if not len(values):
            print("Нет данных")
            exit(0)
        return values, keys

    def csv_filter(self):
        """Фильтрует считываемый csv файл от html тегов и прочего мусора

            Result:
                    Добавляет отфильтрованные данные в новый словарь
                                               """
        reader, list_naming = self.csv_reader()
        for vacancy in reader:
            appendix = {}
            for i in range(len(vacancy)):
                append_item = vacancy[i].strip()
                tag_start = append_item.find("<")
                while tag_start != -1:
                    tag_end = append_item.find(">", tag_start)
                    append_item = append_item.replace(append_item[tag_start: tag_end + 1], "")
                    tag_start = append_item.find("<", tag_start)
                append_item = append_item.strip()
                while append_item.find("  ") != -1: append_item = append_item.replace("  ", " ")
                if append_item.find("\n") != -1: append_item = [" ".join(i.split()) for i in append_item.split("\n")]
                else: append_item = " ".join(append_item.split())
                appendix[list_naming[i]] = append_item
            self.vacancies_objects.append(Vacancy(appendix))

    def filter_vacancies(self, filter_key, filter_val):
        """Фильтрует вакансии по заданным параметрам

                    Args:
                            filter_key: ключ для фильтрации
                            filter_val: значение для фильтрации
                                                       """
        filter_func = formatter[filter_key]
        self.vacancies_objects = list(filter(lambda v: make_filter(filter_func, filter_key, *filter_val)(v.to_dict()),
                                             [vac for vac in self.vacancies_objects]))

    def sort_vacancies(self, name, reverse=False):
        """Сортирует вакансии по заданному значению

                      Args:
                              name: заданное значение
                              reverse: обратный порядок
                                                         """
        self.vacancies_objects = sorted(self.vacancies_objects, key=dic_sorters[name], reverse=reverse)

    def view_vacancies(self, filter_key, filter_val, sort_name, reverse=False):
        """Показывает вакансии с определенными параметрами

                          Args:
                              filter_key: ключ для фильтрации
                              filter_val: значение для фильтрации
                              sort_name: имя для сортировки
                              reverse: обратный порядок
                                                             """
        self.filter_vacancies(filter_key, filter_val)
        self.sort_vacancies(sort_name, reverse)

    def print_vacancies(self, filter_key, filter_val, sort_name, dic_naming, reverse=False, row_indexes=None):
        """Выводит вакансии на экран

                          Args:
                              filter_key: ключ для фильтрации
                              filter_val: значение для фильтрации
                              sort_name: имя для сортировки
                              reverse: обратный порядок
                              dic_naming: название словаря
                              row_indexes: индексы колонок
                                                             """
        if row_indexes is None:
            row_indexes = []
        self.view_vacancies(filter_key, filter_val, sort_name, reverse)
        pretty_vacancies = [vacancy.to_pretty_dict() for vacancy in self.vacancies_objects]
        if not row_indexes: row_indexes = [1, len(pretty_vacancies) + 1]
        if len(row_indexes) == 1: row_indexes = [row_indexes[0], len(pretty_vacancies) + 1]
        added, count = 0, 1
        to_output = PrettyTable(hrules=1, start=row_indexes[0] - 1, end=row_indexes[1] - 1)
        to_output.align = "l"
        for vac in pretty_vacancies:
            if not to_output.field_names:
                to_output.field_names = [name for name in translated_dict.keys() if vac.get(name, None) or name == "№"]
                max_d = {}
                for key in to_output.field_names:
                    max_d[translated_dict[key]] = 20
                to_output._max_width = max_d
            vac["№"] = count
            add = []
            for key in to_output.field_names: add.append(prettify_val(vac.get(key)))
            count, added = count + 1, added + 1
            to_output.add_row(add)
        to_output.field_names = [translated_dict[name] for name in to_output.field_names]
        print(to_output.get_string(fields=list(dic_naming.values()))) if added != 0 and added >= row_indexes[
            0] else print("Ничего не найдено")


class Salary:
    """Класс для представления зарплаты

            Atributs:
                    params: паоаметры
                                                                 """
    def __init__(self, params):
        """Иницилизирует объект Salary, заполняет необходимые поля

                    Atributs:
                            params: паоаметры
                                                                         """
        self.salary_from = params["salary_from"]
        self.salary_to = params["salary_to"]
        self.salary_gross = params["salary_gross"]
        self.salary_currency = params["salary_currency"]


class Vacancy:
    """Класс для преведения данных о вакансиях в нормальный вид

                Atributs:
                        params: паоаметры
                                                                     """
    def __init__(self, params):
        """Иницилизирует объект Vacancy, заполняет необходимые поля

                        Atributs:
                                params: паоаметры
                                                                             """
        self.name = params["name"]
        self.description = params["description"]
        self.key_skills = params["key_skills"]
        self.experience_id = params["experience_id"]
        self.premium = params["premium"]
        self.employer_name = params["employer_name"]
        self.salary = Salary(params)
        self.area_name = params["area_name"]
        self.published_at = params["published_at"]

    def to_dict(self):
        """Добавляет данные в словарь

            Returned:
                    dict: записывает в словарь данные в виде ключ:значение
                                                                     """
        return {"name": self.name, "description": self.description, "key_skills": self.key_skills,
                "experience_id": self.experience_id, "premium": self.premium, "employer_name": self.employer_name,
                "salary_from": self.salary.salary_from, "salary_to": self.salary.salary_to,
                "salary_gross": self.salary.salary_gross, "salary_currency": self.salary.salary_currency,
                "area_name": self.area_name, "published_at": self.published_at}

    def to_pretty_dict(self):
        """Добавляет из словаря в табличку

                    Returned:
                            dict: словарь в виде ключ:значение
                                                                             """
        return {"name": self.name,
                "description": self.description,
                "key_skills": self.key_skills,
                "experience": to_find[self.experience_id],
                "premium": yes_no[self.premium],
                "employer_name": self.employer_name,
                "salary": f"{parse_money(self.salary.salary_from)} - " + f"{parse_money(self.salary.salary_to)} " +
                          f"({to_find[self.salary.salary_currency]}) " + f"({to_find[self.salary.salary_gross]})",
                "area_name": self.area_name,
                "published_at_date": ".".join(self.published_at.split("T")[0].split('-')[::-1])}


class InputConnect:
    """Класс ввода данных пользователем
                                                                     """

    def __init__(self):
        """Инициализирует объект InputConnect
                                                                            """
        self.filename = input("Введите название файла: ")
        filter_params = input("Введите параметр фильтрации: ")
        if ':' not in filter_params and filter_params != "":
            if self.show_problem is None: self.show_problem = "Формат ввода некорректен"
            self.to_making_output = False
        filter_params = filter_params.split(": ")
        if filter_params[0] not in formatter.keys() and filter_params != "":
            if self.show_problem is None: self.show_problem = "Параметр поиска некорректен"
            self.to_making_output = False
        if filter_params != "": self.filter_key, self.filter_val = filter_params[0], filter_params[1:]
        self.sort_param = input("Введите параметр сортировки: ")
        if not (self.sort_param in reversed_dict.keys() or self.sort_param == ""):
            self.to_making_output = False
            if self.show_problem is None: self.show_problem = "Параметр сортировки некорректен"
        sort_reverse_input = input("Обратный порядок сортировки (Да / Нет): ")
        if not (sort_reverse_input in ["Да", "Нет", ""]):
            self.to_making_output = False
            if self.show_problem is None: self.show_problem = "Порядок сортировки задан некорректно"
        if sort_reverse_input == "Да":
            self.reverse = True
        else:
            self.reverse = False
        self.rows = [int(i) for i in input("Введите диапазон вывода: ").split()]
        self.dict_init = {"№": "№"}
        fields = input("Введите требуемые столбцы: ").split(", ")
        if fields and fields != ['']:
            keys = [list(translated_dict.keys())[list(translated_dict.values()).index(i)] for i in fields]
            vals = [translated_dict[key] for key in keys]
            for i in range(len(keys)): self.dict_init[keys[i]] = vals[i]
        else:
            self.dict_init = translated_dict

    to_making_output = True
    show_problem = None
    reverse = False


call_class = InputConnect()


def input_pretty():
    """Функция создает табличку по указаннм параметрам и выводит ее пользователю
                                                                         """

    if call_class.to_making_output:
        ds = DataSet(call_class.filename)
        ds.print_vacancies(call_class.filter_key, call_class.filter_val, call_class.sort_param,
                           call_class.dict_init, call_class.reverse, call_class.rows)
    else: print(call_class.show_problem)


input_pretty()

# Введите название файла: vacancies.csv
# Введите параметр фильтрации: Опыт работы: От 3 до 6 лет
# Введите параметр сортировки: Оклад
# Обратный порядок сортировки (Да / Нет): Нет
# Введите диапазон вывода: 10 20
# Введите требуемые столбцы: Название, Навыки, Опыт работы, Компания
