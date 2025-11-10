from typing import Any, Dict
from src.api_request import HHAPI


class DummyResponse:
    def __init__(self, json_data: Dict[str, Any], status_code: int = 200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("bad status")


def test_hhapi_returns_items(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert "vacancies" in url  # убедимся, что по правильному URL
        # вернём структуру как у hh
        return DummyResponse(
            {
                "items": [
                    {"name": "Python Dev"},
                    {"name": "Go Dev"},
                ]
            }
        )

    monkeypatch.setattr("api_request.requests.get", fake_get)

    api = HHAPI()
    items = api.get_vacancies("python", per_page=2)

    assert isinstance(items, list)
    assert len(items) == 2
    assert items[0]["name"] == "Python Dev"
