from datetime import datetime
from decimal import Decimal

import pytest
from src.bot import Bot, Currency, User


@pytest.fixture()
def default_user():
    data = {
        'login': 'test',
        'id': 1,
        'money': Decimal('100'),
    }
    return User(**data)


@pytest.fixture()
def default_currency():
    data = {
        'name': 'test',
        'time': datetime.now(),
        'purchasing_price': Decimal('1.488'),
        'selling_price': Decimal('1.337'),
    }

    return Currency(**data)


@pytest.fixture()
def bot():
    return Bot(1, Decimal('1.0'), Decimal('1.0'))


@pytest.fixture()
def mock_post(mocker):
    return mocker.patch('requests.post')


@pytest.fixture()
def mock_get(mocker):
    return mocker.patch('requests.get')


def test_add_user(mock_post):
    mock_post.return_value.json.return_value = dict(
        id='1', login='login', money=str(Decimal('100'))
    )
    user = Bot.add_user('login')
    assert user.login == 'login'
    assert user.id == 1
    assert user.money == Decimal('100')


def test_get_currency(mock_get):
    name = 'bitcoin'
    purchasing_price = '2.63'
    selling_price = '2.49'
    mock_get.return_value.json.return_value = {
        'name': name,
        'purchasing_price': purchasing_price,
        'selling_price': selling_price,
        'time': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
    }
    currency = Bot.get_currency(1)
    assert currency.name == name
    assert currency.purchasing_price == Decimal(purchasing_price)
    assert currency.selling_price == Decimal(selling_price)


@pytest.fixture()
def mock_add_user(mocker, default_user):
    mocker.patch.object(Bot, 'add_user')
    Bot.add_user.return_value = default_user


@pytest.fixture()
def mock_get_currency(mocker, default_currency):
    mocker.patch.object(Bot, 'get_currency')
    Bot.get_currency.return_value = default_currency


@pytest.mark.usefixtures('mock_add_user', 'mock_get_currency')
def test_buy(mocker, bot):
    mocker.patch.object(Bot, 'buy')
    assert bot.start_buy().name == 'test'
