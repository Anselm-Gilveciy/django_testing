from pytest_lazyfixture import lazy_fixture

ADMIN = lazy_fixture('admin_client')
"""Зарегистрированный пользователь."""

AUTHOR = lazy_fixture('author_client')
"""Автор комментария."""

CLIENT = lazy_fixture('client')
"""Анонимный пользователь."""

PK = lazy_fixture('pk_news')
"""Первичеый ключ новости."""

URL = {
    'home': 'news:home',
    'detail': 'news:detail',
    'edit': 'news:edit',
    'delete': 'news:delete',
    'login': 'users:login',
    'logout': 'users:logout',
    'signup': 'users:signup',
}
"""Словарь для провеки страниц приложения."""
