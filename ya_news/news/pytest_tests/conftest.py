from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Автор комментария."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    """Залогиненный автор комментария."""
    client.force_login(author)
    return client


@pytest.fixture
def news():
    """Данные новости."""
    return News.objects.create(
        title='Заголовок новости',
        text='Текст новости'
    )


@pytest.fixture
def pk_news(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    """Данные комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_list():
    """Список новостей."""
    today = datetime.today()
    news_list = News.objects.bulk_create(
        News(
            title=f'Заголовок новости {index}',
            text=f'Текст новости {index}',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_list


@pytest.fixture
def comments_list(author, news):
    """Список комментариев."""
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}.'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
    return comments_list


@pytest.fixture
def form_data():
    """Форма с данными нового комментария.."""
    return {
        'text': 'Новый комментарий'
    }
