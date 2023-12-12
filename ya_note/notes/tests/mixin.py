from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestMixinCreatNoteConstant(TestCase):
    """Данные для новой заметки."""

    NOTE_TITLE = 'Тестовая заметка.'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug-test-1'


class TestMixinUpdateNoteConstant(TestCase):
    """Данные для обновления заметки."""

    NEW_NOTE_TITLE = 'New Тестовая заметка.'
    NEW_NOTE_TEXT = 'New Текст заметки'
    NEW_NOTE_SLUG = 'new-slug-test-1'


class TestMixinAuthor(TestCase):
    """Миксин для создания автора заметки."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Фамилия Имя')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)


class TestMixinNote(TestMixinAuthor):
    """Миксин для создания заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author)


class TestMixinAuthorNoteReader(TestMixinNote):
    """Миксин для создания читателя заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)


class TestMixinNoteCreate(TestMixinAuthor):
    """Миксин для формы создания заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG}


class TestMixinNoteEditDelete(TestMixinAuthorNoteReader):
    """Миксин для удаления и редактирование заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.success_url = reverse('notes:success')
        cls.url_edit = reverse('notes:edit', kwargs={'slug': cls.note.slug})
        cls.url_delete = reverse('notes:delete', kwargs={
            'slug': cls.note.slug})
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NEW_NOTE_SLUG}


class TestCheck(TestCase):
    """Миксин для проверки корректности заметки."""

    def check(self, notes, title, text, slug):
        data = (notes.title, notes.text, notes.slug)
        const_data = (title, text, slug)
        for db_value, value in zip(
            data, const_data
        ):
            with self.subTest(db_value=db_value, value=value):
                self.assertEqual(
                    db_value,
                    value
                )
