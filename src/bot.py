from decimal import Decimal
from typing import NamedTuple

import requests
from requests import Response


class User(NamedTuple):
    login: str
    id: int
    money: Decimal


class Bot:
    @staticmethod
    def add_user(login: str) -> User:
        response: Response = requests.post(
            'http://localhost:5000/users/', dict(login=login)
        )
        res = response.json()
        return User(res['login'], int(res['id']), Decimal(res['money']))
