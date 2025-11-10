from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Vacancy:
    """
    Класс-вакансия.

    """
    title: str
    url: str
    salary: int
    description: str
    employer: str | None = None

    def __post_init__(self):
        # Валидация зарплаты: если не указана или отрицательная — ставим 0
        if self.salary is None or self.salary < 0:
            self.salary = 0

    @classmethod
    def from_hh(cls, raw: dict) -> "Vacancy":
        """
        Создаёт Vacancy из словаря, который пришёл от hh.ru
        """
        name = raw.get("name", "Без названия")
        url = raw.get("alternate_url", "")
        snippet = raw.get("snippet") or {}
        desc = snippet.get("responsibility") or snippet.get("requirement") or ""

        salary_block = raw.get("salary")
        salary_value = 0
        if salary_block:

            if salary_block.get("from"):
                salary_value = salary_block["from"]
            elif salary_block.get("to"):
                salary_value = salary_block["to"]

        employer = None
        if raw.get("employer"):
            employer = raw["employer"].get("name")

        return cls(
            title=name,
            url=url,
            salary=salary_value or 0,
            description=desc or "",
            employer=employer,
        )

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary < other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        return self.salary > other.salary

    def __repr__(self) -> str:
        return f"Vacancy({self.title!r}, salary={self.salary})"
