from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note

from pytils.translit import slugify

from .mixin import (TestCheck, TestMixinCreatNoteConstant, TestMixinNoteCreate,
                    TestMixinNoteEditDelete, TestMixinUpdateNoteConstant)

User = get_user_model()


class TestNoteCreation(
    TestMixinCreatNoteConstant, TestCheck, TestMixinNoteCreate
):
    """Проверки создания заметок."""

    def test_user_can_create_note(self):
        """Пользователь может создать заметку."""
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        notes = Note.objects.last()
        self.check(notes, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)

    def test_anonymous_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        note_count_current = Note.objects.count()
        self.client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)

    def test_unique_slug_field(self):
        """Проверка уникальности slug."""
        Note.objects.create(
            title=self.NOTE_TITLE,
            text=self.NOTE_TEXT,
            slug=self.NOTE_SLUG,
            author=self.author,
        )
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertFormError(response,
                             form='form', field='slug',
                             errors=f'{self.NOTE_SLUG}{WARNING}')

    def test_generate_slug_if_field_empty(self):
        """Проверка, что slug формируется из title."""
        self.form_data.pop('slug')
        expected_slug = slugify(self.form_data['title'])
        self.assertRedirects(
            self.author_client.post(self.url, data=self.form_data),
            self.success_url
        )
        self.author_client.post(self.url, data=self.form_data)
        note = Note.objects.last()
        self.assertEqual(expected_slug, note.slug)


class TestNoteEditDelete(TestMixinCreatNoteConstant,
                         TestCheck,
                         TestMixinUpdateNoteConstant,
                         TestMixinNoteEditDelete):
    """Проверки редактирования и удаления заметок."""

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        note_count_current = Note.objects.count()
        response = self.author_client.delete(self.url_delete)
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current - 1, note_count)

    def test_user_cant_delete_note_of_another_user(self):
        """Пользователь не может удалить чужую заметку."""
        note_count_current = Note.objects.count()
        response = self.reader_client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)

    def test_author_can_edit_note(self):
        """Автор может изменить свою заметку."""
        response = self.author_client.post(self.url_edit, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        notes = Note.objects.last()
        self.check(
            notes,
            self.NEW_NOTE_TITLE,
            self.NEW_NOTE_TEXT,
            self.NEW_NOTE_SLUG
        )

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может изменить чужую заметку."""
        response = self.reader_client.post(self.url_edit, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        notes = Note.objects.last()
        self.check(notes, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)
