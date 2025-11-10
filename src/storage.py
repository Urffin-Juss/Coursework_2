from __future__ import annotations
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from src.vacancy import Vacancy


class BaseStorage(ABC):

    @abstractmethod
    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        pass

    @abstractmethod
    def load_vacancies(self) -> None:
        pass

    @abstractmethod
    def add_vacancy(self, vacancies: Vacancy) -> None:
        pass

    @abstractmethod
    def delet_vacancy(self, title: str) -> None:
        pass



class JSONStorage(BaseStorage):

    def __init__(self, filepath: str = "data/vacancies.json") -> None:
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.write_text("[]", encoding="utf-8")


    def save_vacancies(self, vacancies: List[Vacancy]) -> None:
        data = [
            {
                "title": v.title,
                "url": v.url,
                "salary": v.salary,
                "description": v.description,
                "employer": v.employer,
            }
            for v in vacancies
        ]
        self.filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_vacancies(self) -> List[Vacancy]:
        raw_text = self.filepath.read_text(encoding="utf-8")
        raw_list = json.loads(raw_text)
        vacancies: List[Vacancy] = []
        for item in raw_list:
            vacancies.append(
                Vacancy(
                    title=item["title"],
                    url=item["url"],
                    salary=item.get("salary", 0),
                    description=item.get("description", ""),
                    employer=item.get("employer"),
                )
            )
        return vacancies

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.load_vacancies()
        vacancies.append(vacancy)
        self.save_vacancies(vacancies)

    def delete_vacancy(self, title: str) -> None:
        vacancies = self.load_vacancies()
        filtered = [v for v in vacancies if v.title != title]
        self.save_vacancies(filtered)



