from decimal import Decimal

from src.bot import Bot


def test_add_user(mocker):
    post = mocker.patch('requests.post')
    post.return_value.json.return_value = dict(
        id='1', login='login', money=str(Decimal('100'))
    )
    user = Bot.add_user('login')
    assert user.login == 'login'
    assert user.id == 1
    assert user.money == Decimal('100')
