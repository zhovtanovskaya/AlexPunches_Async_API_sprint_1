"""Тесты Пользователя."""
from http import HTTPStatus

import pytest

from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


@pytest.mark.parametrize('user', [faker_data.users[0]])
def test_login_history_list(db_insert_fake_data, admin_action, user):
    """Админ может получить историю входов пользователя."""
    response = admin_action.get_user_login_histories(
        user.id, page_number=1, per_page=1,
    )
    assert response.status_code == HTTPStatus.OK

    login_history = response.json()
    assert len(login_history.get('login_histories')) == 1
    assert login_history.get('total_items') == 10
