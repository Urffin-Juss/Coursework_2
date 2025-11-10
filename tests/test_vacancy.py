from vacancy import Vacancy


def test_vacancy_init_and_validation():
    v = Vacancy(
        title="Python Dev",
        url="https://hh.ru/vacancy/1",
        salary=-100,
        description="Cool job",
        employer="SkyPro",
    )

    # зарплата должна была стать 0
    assert v.salary == 0
    assert v.title == "Python Dev"
    assert "Cool" in v.description


def test_vacancy_from_hh_parses_salary_from():
    raw = {
        "name": "Backend",
        "alternate_url": "https://hh.ru/vacancy/2",
        "salary": {"from": 150000, "to": 200000, "currency": "RUR"},
        "snippet": {"requirement": "Python, Django"},
        "employer": {"name": "Company"},
    }

    v = Vacancy.from_hh(raw)

    assert v.title == "Backend"
    assert v.salary == 150000
    assert v.employer == "Company"
    assert "Python" in v.description


def test_vacancy_compare_by_salary():
    v1 = Vacancy("A", "u", 100, "", None)
    v2 = Vacancy("B", "u", 200, "", None)

    assert v2 > v1
    assert not v1 > v2
    assert v1 < v2
