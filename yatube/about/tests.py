from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

User = get_user_model()


class AboutURLTests(TestCase):
    """Создаем тестовый пост и группу."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='leo')

    def setUp(self):
        """Создаем клиент гостя и зарегистрированного пользователя."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(AboutURLTests.user)

    def test_urls_response_guest(self):
        """Проверяем статус страниц для гостя."""
        url_status = [
            (reverse('about:author'), HTTPStatus.OK),
            (reverse('about:tech'), HTTPStatus.OK)
        ]
        for url, status_code in url_status:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """Проверяем запрашиваемые шаблоны страниц через имена."""
        cache.clear()
        templates_pages_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
