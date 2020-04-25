from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel
from requests import Response


class User(BaseModel):
    login: str
    id: int
    money: Decimal


class Currency(BaseModel):
    name: str
    time: datetime
    purchasing_price: Decimal
    selling_price: Decimal


class Bot:
    URL: str = 'http://localhost:5000'

    def __init__(self, currency_id: int, profit: Decimal, money: Decimal) -> None:
        self.currency_id: int = currency_id
        self.profit: Decimal = profit
        self.money: Decimal = money
        self.amount: Optional[Decimal] = None
        self.currency_name: Optional[str] = None
        self.user_id: Optional[int] = None

    def start_buy(self) -> Currency:
        self.user_id = Bot.add_user('login').id
        purchased_currency = Bot.get_currency(self.currency_id)
        self.amount = self.money / purchased_currency.purchasing_price
        self.currency_name = purchased_currency.name
        Bot.buy(self.user_id, self.currency_id, self.amount, purchased_currency.time)
        return purchased_currency

    @staticmethod
    def add_user(login: str) -> User:
        response: Response = requests.post(Bot.URL + '/users/', dict(login=login))
        res: Dict[str, Any] = response.json()
        return User(**res)

    @staticmethod
    def get_currency(currency_id: int) -> Currency:
        response: Response = requests.get(Bot.URL + f'/currencies/{currency_id}/')
        res: Dict[str, Any] = response.json()
        return Currency(**res)

    @staticmethod
    def _operate(
        user_id: int,
        currency_id: int,
        amount: Decimal,
        time: datetime,
        operation_type: str,
    ) -> Response:
        response: Response = requests.post(
            Bot.URL + f'/users/{user_id}/currencies/',
            dict(
                currency_id=currency_id,
                amount=str(amount),
                operation=operation_type,
                time=datetime.strftime(time, '%Y-%m-%d %H:%M:%S'),
            ),
        )

        return response

    @staticmethod
    def buy(
        user_id: int, currency_id: int, amount: Decimal, time: datetime
    ) -> Response:
        response: Response = Bot._operate(user_id, currency_id, amount, time, 'BUY')
        return response

    @staticmethod
    def sell(
        user_id: int, currency_id: int, amount: Decimal, time: datetime
    ) -> Response:
        response: Response = Bot._operate(user_id, currency_id, amount, time, 'SELL')
        return response
