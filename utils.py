import requests
import psycopg2

# Список id работодателей для сбора вакансий
list_employers_id = ['2180', '3529', '4394', '955', '1740', '816144', '2748', '80', '49357', '78638']


def get_employers_data():
    """Получение данных о работодателях с помощью API HeadHunter."""
    url = 'https://api.hh.ru/employers/'
    params = {
        'page': 10,
        'per_page': 100
    }
    employers = []
    for emp in list_employers_id:
        response = requests.get(url + f'{emp}', params=params, headers={"User-Agent": "HH-User-Agent"}).json()
        employers.append({'employer_id': response.get("id"),
                          'employer_name': response.get("name"),
                          'open_vacancies': response.get("open_vacancies")
                          })
    return employers


def get_vacancies_data():
    """Получение данных о вакансиях с помощью API HeadHunter."""
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'page': 0,
        'per_page': 50
    }
    vacancies = []
    for emp in list_employers_id:
        response = requests.get(url + f'?employer_id={emp}', params=params,
                                headers={"User-Agent": "HH-User-Agent"}).json()
        for vac in response['items']:
            try:
                vacancy = {'vacancy_id': vac['id'],
                           'vacancy_name': vac["name"],
                           'salary_min': vac['salary']["from"],
                           'url': vac["alternate_url"],
                           'description': vac['snippet']["requirement"],
                           'employer_name': vac['employer']["name"],
                           'employer_id': vac['employer']["id"]}
            except(TypeError, IndexError, ValueError, KeyError):
                vacancy = {'vacancy_id': vac['id'],
                           'vacancy_name': vac["name"],
                           'salary_min': 0,
                           'url': vac["alternate_url"],
                           'description': vac['snippet']["requirement"],
                           'employer_name': vac['employer']["name"],
                           'employer_id': vac['employer']["id"]}
            vacancies.append(vacancy)
    return vacancies


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и работодателях."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")


    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) UNIQUE NOT NULL,
                open_vacancies INTEGER)
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR(250) NOT NULL,
                salary_min INTEGER,
                url TEXT,
                employer_name VARCHAR REFERENCES employers(employer_name),
                employer_id INT REFERENCES employers(employer_id))
        """)

    conn.commit()
    conn.close()


def save_data_to_database(database_name: str, params: dict):
    """Сохранение данных о вакансиях и работодателях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    employers = get_employers_data()
    vacancies = get_vacancies_data()
    with conn.cursor() as cur:
        for emp in employers:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, open_vacancies)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (emp['employer_id'], emp['employer_name'], emp['open_vacancies'])
            )

        for vac in vacancies:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, salary_min, url, employer_name, employer_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                
                """,
                (vac['vacancy_id'], vac['vacancy_name'], vac['salary_min'], vac['url'],
                 vac['employer_name'], vac['employer_id'])
            )

    conn.commit()
    conn.close()



