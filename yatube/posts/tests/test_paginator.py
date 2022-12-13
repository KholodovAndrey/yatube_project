from random import randint

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Group
from ..utils import POSTS_PER_PAGE

User = get_user_model()

POSTS_VT_PAGE = randint(0, POSTS_PER_PAGE)
POST_ALL = POSTS_PER_PAGE + POSTS_VT_PAGE


class PaginatorViewTests(TestCase):
    """Создаем тестовые посты и группы."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='leo')
        cls.group = Group.objects.create(
            title='Группа поклонников графа',
            slug='tolstoi',
            description='Что-то о группе'
        )
        paginator_objects = []
        for i in range(POST_ALL):
            new_post = Post(
                author=PaginatorViewTests.user,
                text='Тестовый пост ' + str(i),
                group=PaginatorViewTests.group
            )
            paginator_objects.append(new_post)
        Post.objects.bulk_create(paginator_objects)
        cls.paginator_data = {
            'index': reverse('posts:index'),
            'group': reverse(
                'posts:group_list',
                kwargs={'slug': PaginatorViewTests.group.slug}
            ),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': PaginatorViewTests.user.username}
            )
        }

    def test_per_page_paginator_correct_context(self):
        """Шаблон 1 страницы index, group_list и profile
        сформированы с корректным Paginator.
        """
        for (
            paginator_place,
            paginator_page
        ) in PaginatorViewTests.paginator_data.items():
            with self.subTest(paginator_place=paginator_place):
                response_page_1 = self.client.get(paginator_page)
                self.assertEqual(len(
                    response_page_1.context['page_obj']),
                    POSTS_PER_PAGE
                )

    def test_vt_page_paginator_correct_context(self):
        """Шаблон 2 страницы index, group_list и profile
        сформированы с корректным Paginator.
        """
        for (
            paginator_place,
            paginator_page
        ) in PaginatorViewTests.paginator_data.items():
            with self.subTest(paginator_place=paginator_place):
                response_page_2 = self.client.get(
                    paginator_page + '?page=2'
                )
                self.assertEqual(len(
                    response_page_2.context['page_obj']),
                    POSTS_VT_PAGE
                )
