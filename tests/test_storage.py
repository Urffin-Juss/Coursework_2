from pathlib import Path

from vacancy import Vacancy
from storage import JSONStorage


def test_json_storage_save_and_load(tmp_path: Path):
    file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(file))

    v1 = Vacancy("Python Dev", "https://hh.ru/v/1", 150000, "desc", "Company")
    v2 = Vacancy("Go Dev", "https://hh.ru/v/2", 120000, "desc2", "Company2")

    storage.save_vacancies([v1, v2])

    loaded = storage.load_vacancies()

    assert len(loaded) == 2
    assert loaded[0].title == "Python Dev"
    assert loaded[1].salary == 120000


def test_json_storage_add_and_delete(tmp_path: Path):
    file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(file))

    v1 = Vacancy("Python Dev", "https://hh.ru/v/1", 150000, "desc", "Company")

    storage.add_vacancy(v1)
    assert len(storage.load_vacancies()) == 1

    storage.delete_vacancy("Python Dev")
    assert len(storage.load_vacancies()) == 0
