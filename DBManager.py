import psycopg2
from config import config


class DBManager:

    def __init__(self, database_name):
        self.database_name = database_name

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("SELECT employer_name, open_vacancies FROM employers")
            data = cur.fetchall()
            conn.close()
            return data

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
         и ссылки на вакансию."""
        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("SELECT employer_name, vacancy_name, salary_min, url FROM vacancies")
            data = cur.fetchall()
            conn.close()
            return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_min) FROM vacancies")
            data = cur.fetchall()
            conn.close()
            return data

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies)")
            data = cur.fetchall()
            conn.close()
            return data

    def get_vacancies_with_keyword(self, keytext):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name ILIKE '%{keytext}%'")
            data = cur.fetchall()
            conn.close()
            return data
