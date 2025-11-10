from abc import ABC, abstractmethod
from typing import Any, Dict, List
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self, *arg, **kwargs) -> list[Dict[str, Any]:
        pass


class HH_API(BaseAPI):
        BASE_URL = os.getenv('HH_API_URL')


        def get_vacancies(
                self,
                text: str,
                page: int = 0,
                per_page: int = 50,
                area: int = 123,
        ): -> list[Dict[str, Any]]:
                params = {
                    "text" : text,
                    "page" : page,
                    "per_page" : per_page,
                    "area" : area,
                }
                resp = requests.get(self.BASE_URL, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get("items", [])

