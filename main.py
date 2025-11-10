import dotenv
import os
from src.vacancy import Vacancy
from src.storage import JSONStorage

load_dotenv()


def main():
    api = HHAPI()
    raw_vacancies = api.get_vacancies("python разработчик", per_page=20)

    vacancies = [Vacancy.from_hh(item) for item in raw_vacancies]

    storage = JSONStorage("data/vacancies.json")
    storage.save_vacancies(vacancies)

    # пример фильтрации
    rich = [v for v in vacancies if v.salary >= 150_000]
    for v in rich:
        print(v)


if __name__ == "__main__":
    main()
