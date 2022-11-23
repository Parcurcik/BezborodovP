import csv
from openpyxl import Workbook
import matplotlib


class Vacancy:
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

    def __init__(self, vacancy):
        self.name = vacancy['name']
        self.salary_from = int(float(vacancy['salary_from']))
        self.salary_to = int(float(vacancy['salary_to']))
        self.salary_currency = vacancy['salary_currency']
        self.salary_average = self.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2
        self.area_name = vacancy['area_name']
        self.year = int(vacancy['published_at'][:4])


def average(dictionary):
    new_dict = {}
    for key, values in dictionary.items(): new_dict[key] = int(sum(values) / len(values))
    return new_dict


def print_statistic(years_level, vac_number, din_for_changed, din_for_years, level_cityes, dol_vac):
    print('Динамика уровня зарплат по годам: {0}'.format(years_level))
    print('Динамика количества вакансий по годам: {0}'.format(vac_number))
    print('Динамика уровня зарплат по годам для выбранной профессии: {0}'.format(din_for_changed))
    print('Динамика количества вакансий по годам для выбранной профессии: {0}'.format(din_for_years))
    print('Уровень зарплат по городам (в порядке убывания): {0}'.format(level_cityes))
    print('Доля вакансий по городам (в порядке убывания): {0}'.format(dol_vac))


def find_increment(dictionary, key, amount):
    if key in dictionary: dictionary[key] += amount
    else: dictionary[key] = amount


class DataSet:
    def __init__(self, file_name, vacancy_name):
        self.file_name = file_name
        self.vacancy_name = vacancy_name

    def csv_reader(self):
        with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            header = next(reader)
            header_length = len(header)
            for row in reader:
                if '' not in row and len(row) == header_length:
                    yield dict(zip(header, row))

    def get_statistic(self):
        salary = {}
        salary_of_vacancy_name = {}
        salary_city = {}
        count_of_vacancies = 0

        for vacancy_dictionary in self.csv_reader():
            vacancy = Vacancy(vacancy_dictionary)
            find_increment(salary, vacancy.year, [vacancy.salary_average])
            if vacancy.name.find(self.vacancy_name) != -1: find_increment(salary_of_vacancy_name, vacancy.year, [vacancy.salary_average])
            find_increment(salary_city, vacancy.area_name, [vacancy.salary_average])
            count_of_vacancies += 1

        vacancies_number = dict([(key, len(value)) for key, value in salary.items()])
        vacancies_number_by_name = dict([(key, len(value)) for key, value in salary_of_vacancy_name.items()])

        if not salary_of_vacancy_name:
            salary_of_vacancy_name = dict([(key, [0]) for key, value in salary.items()])
            vacancies_number_by_name = dict([(key, 0) for key, value in vacancies_number.items()])

        first_stat = average(salary)
        second_stat = average(salary_of_vacancy_name)
        thired_stat = average(salary_city)

        fourth_stat = {}
        for year, salaries in salary_city.items():
            fourth_stat[year] = round(len(salaries) / count_of_vacancies, 4)
        fourth_stat = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in fourth_stat.items()]))
        fourth_stat.sort(key=lambda a: a[-1], reverse=True)
        fifth_stats = fourth_stat.copy()
        fourth_stat = dict(fourth_stat)
        thired_stat = list(filter(lambda a: a[0] in list(fourth_stat.keys()), [(key, value) for key, value in thired_stat.items()]))
        thired_stat.sort(key=lambda a: a[-1], reverse=True)
        thired_stat = dict(thired_stat[:10])
        fifth_stats = dict(fifth_stats[:10])

        return first_stat, vacancies_number, second_stat, vacancies_number_by_name, thired_stat, fifth_stats


class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        dataset = DataSet(self.file_name, self.vacancy_name)
        first_stat, second_stat, thired_stat, fourth_stat, fifth_stats, sixth_stat = dataset.get_statistic()
        print_statistic(first_stat, second_stat, thired_stat, fourth_stat, fifth_stats, sixth_stat)



def make_column_width(column_widths, cell, i):
    if len(column_widths) > i:
        if len(cell) > column_widths[i]:
            column_widths[i] = len(cell)
    else: column_widths += [len(cell)]



if __name__ == '__main__':
    InputConnect()
