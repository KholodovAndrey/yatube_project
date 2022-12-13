from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, POSTS_AMOUNT_SYMBOLS

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='leo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_posts_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text[:POSTS_AMOUNT_SYMBOLS]
        self.assertEqual(expected_object_name, str(post))

    def test_models_have_correct_group_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_verbose_name(self):
        """verbose_name поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        verboses = {
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_help_text(self):
        """help_text поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        help_text = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected_value in help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
