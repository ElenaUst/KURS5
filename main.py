from utils import create_database, save_data_to_database
from config import config
from FormatManager import FormatManager


def main():
    params = config()
    database_name = 'hhdatabase'
    create_database(database_name, params)
    save_data_to_database(database_name, params)
    while True:
        user_input = input("""
1 - Получить список компаний и количество открытых вакансий,
2 - Получить все вакансии,
3 - Получить среднюю зарплату по всем вакансиям,
4 - Получить все вакансии с зарплатой выше средней,
5 - Получить список вакансий по ключевому слову,
6 - Выйти из программы.
        \n""")
        if user_input == '1':
            fm = FormatManager(database_name)
            fm.format_get_companies_and_vacancies_count()
        elif user_input == '2':
            fm = FormatManager(database_name)
            fm.format_get_all_vacancies()
        elif user_input == '3':
            fm = FormatManager(database_name)
            fm.format_get_avg_salary()
        elif user_input == '4':
            fm = FormatManager(database_name)
            fm.format_get_vacancies_with_higher_salary()
        elif user_input == '5':
            keytext = input("""Введите ключевое слово для поиска вакансий:""")
            fm = FormatManager(database_name)
            fm.format_get_vacancies_with_keyword(keytext)
        elif user_input == '6':
            break
        else:
            print('Данное действие недоступно, попробуйте еще раз')


if __name__ == '__main__':
    main()
