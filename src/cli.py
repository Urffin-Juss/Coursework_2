from typing import List
from src.api_request import HHAPI
from src.vacancy import Vacancy
from src.storage import JSONStorage


def fetch_and_convert(query: str, limit: int = 50) -> List[Vacancy]:
    api = HHAPI()
    raw = api.get_vacancies(query, per_page=limit)
    return [Vacancy.from_hh(item) for item in raw]


def show_top_by_salary(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    # сортируем по зарплате по убыванию
    sorted_vac = sorted(vacancies, key=lambda v: v.salary, reverse=True)
    return sorted_vac[:n]


def filter_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    keyword_lower = keyword.lower()
    return [
        v
        for v in vacancies
        if keyword_lower in (v.description or "").lower()
        or keyword_lower in (v.title or "").lower()
    ]


def run_cli():
    print("=== Поиск вакансий с hh.ru ===")
    query = input("Введите поисковый запрос (например, 'python разработчик'): ").strip()
    if not query:
        print("Пустой запрос — нечего искать.")
        return

    print("Получаю вакансии с hh.ru ...")
    vacancies = fetch_and_convert(query, limit=50)
    print(f"Найдено вакансий: {len(vacancies)}")

    storage = JSONStorage("data/vacancies.json")
    storage.save_vacancies(vacancies)
    print("Вакансии сохранены в data/vacancies.json")

    while True:
        print("\nВыберите действие:")
        print("1 — показать топ N вакансий по зарплате")
        print("2 — отфильтровать вакансии по ключевому слову")
        print("3 — показать все вакансии (коротко)")
        print("0 — выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            n_str = input("Сколько вакансий показать? ").strip()
            n = int(n_str) if n_str.isdigit() else 5
            top_vac = show_top_by_salary(vacancies, n)
            for v in top_vac:
                print(f"{v.title} — {v.salary} руб. — {v.url}")
        elif choice == "2":
            kw = input("Ключевое слово: ").strip()
            filtered = filter_by_keyword(vacancies, kw)
            print(f"Найдено {len(filtered)} вакансий по слову '{kw}':")
            for v in filtered:
                print(f"{v.title} — {v.salary} руб. — {v.url}")
        elif choice == "3":
            for v in vacancies:
                print(f"{v.title} — {v.salary} руб.")
        elif choice == "0":
            print("Пока 👋")
            break
        else:
            print("Неизвестная команда, попробуйте снова.")
