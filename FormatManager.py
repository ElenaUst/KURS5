from DBManager import DBManager


class FormatManager:

    def __init__(self, database_name):
        self.database_name = database_name

    def format_get_companies_and_vacancies_count(self):
        db_manager = DBManager(self.database_name)
        data = db_manager.get_companies_and_vacancies_count()

        for d in data:
            print(f'Название компании: {d[0]}\n'f'Количество открытых вакансий: {d[1]}\n')

    def format_get_all_vacancies(self):
        db_manager = DBManager(self.database_name)
        data = db_manager.get_all_vacancies()

        for d in data:
            print(
                f'Название вакансии: {d[1]}\n'f'Зарплата: {d[2]}\n'f'Ссылка на вакансию: {d[3]}\n'f'Название компании: {d[0]}\n')

    def format_get_avg_salary(self):
        db_manager = DBManager(self.database_name)
        data = db_manager.get_avg_salary()

        for d in data:
            print(f'Средняя зарплата по всем вакансиям: {d[0]}\n')

    def format_get_vacancies_with_higher_salary(self):
        db_manager = DBManager(self.database_name)
        data = db_manager.get_vacancies_with_higher_salary()

        for d in data:
            print(
                f'Название вакансии: {d[1]}\n'f'Зарплата: {d[2]}\n'f'Ссылка на вакансию: {d[3]}\n'f'Название компании: {d[4]}\n')

    def format_get_vacancies_with_keyword(self, keytext):
        db_manager = DBManager(self.database_name)
        data = db_manager.get_vacancies_with_keyword(keytext)

        for d in data:
            print(
                f'Название вакансии: {d[1]}\n'f'Зарплата: {d[2]}\n'f'Ссылка на вакансию: {d[3]}\n'f'Название компании: {d[4]}\n')
