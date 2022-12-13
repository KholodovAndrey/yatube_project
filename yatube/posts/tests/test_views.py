import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from ..models import Post, Group, Follow

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTests(TestCase):
    """Создаем тестовые посты и группы."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='leo')
        cls.group = Group.objects.create(
            title='Группа поклонников графа',
            slug='tolstoi',
            description='Что-то о группе'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Война и мир изначально назывался «1805 год»',
            group=cls.group,
            image=uploaded
        )
        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые медиа."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Создаем клиент зарегистрированного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewTests.user)
        cache.clear()

    def post_exist(self, page_context):
        """Метод для проверки существования поста на страницах."""
        if 'page_obj' in page_context:
            post = page_context['page_obj'][0]
        else:
            post = page_context['post']
        post_author = post.author
        post_text = post.text
        task_image = post.image
        post_group = post.group
        self.assertEqual(
            post_author,
            PostViewTests.post.author
        )
        self.assertEqual(
            post_text,
            PostViewTests.post.text
        )
        self.assertEqual(
            task_image,
            PostViewTests.post.image
        )
        self.assertEqual(
            post_group,
            PostViewTests.post.group
        )

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response_index = self.authorized_client.get(reverse('posts:index'))
        page_index_context = response_index.context
        self.post_exist(page_index_context)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response_post_detail = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostViewTests.post.pk}
            )
        )
        page_post_detail_context = response_post_detail.context
        self.post_exist(page_post_detail_context)

    def test_group_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response_group = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostViewTests.group.slug}
            )
        )
        page_group_context = response_group.context
        task_group = response_group.context['group']
        self.post_exist(page_group_context)
        self.assertEqual(task_group, PostViewTests.group)

    def test_profile_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response_profile = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostViewTests.user.username}
            )
        )
        page_profile_context = response_profile.context
        task_profile = response_profile.context['author']
        self.post_exist(page_profile_context)
        self.assertEqual(task_profile, PostViewTests.user)

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = PostViewTests.form_fields
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон create_post(edit) сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': PostViewTests.post.pk})
        )
        form_fields = PostViewTests.form_fields
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_index_caches(self):
        """Тестирование кэша главной страницы."""
        new_post = Post.objects.create(
            author=PostViewTests.user,
            text='Этот пост для проверки кэширования',
            group=PostViewTests.group
        )
        response_1 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_content_1 = response_1.content
        new_post.delete()
        response_2 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_content_2 = response_2.content
        self.assertEqual(response_content_1, response_content_2)
        cache.clear()
        response_3 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_content_3 = response_3.content
        self.assertNotEqual(response_content_2, response_content_3)

    def test_follow(self):
        """Тестирование подписки на автора."""
        count_follow = Follow.objects.count()
        new_author = User.objects.create(username='Lermontov')
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': new_author.username}
            )
        )
        follow = Follow.objects.last()
        self.assertEqual(Follow.objects.count(), count_follow + 1)
        self.assertEqual(follow.author, new_author)
        self.assertEqual(follow.user, PostViewTests.user)

    def test_unfollow(self):
        """Тестирование отписки от автора."""
        count_follow = Follow.objects.count()
        new_author = User.objects.create(username='Lermontov')
        Follow.objects.create(user=self.user, author=new_author)
        self.assertTrue(Follow.objects.count(), count_follow + 1)
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': new_author.username}
            )
        )
        self.assertEqual(Follow.objects.count(), count_follow)

    def test_following_posts(self):
        """Тестирование появления поста автора в ленте подписчика."""
        new_user = User.objects.create(username='Lermontov')
        authorized_client = Client()
        authorized_client.force_login(new_user)
        Follow.objects.create(user=new_user, author=self.user)
        response_follow = authorized_client.get(
            reverse('posts:follow_index')
        )
        context_follow = response_follow.context
        self.post_exist(context_follow)

    def test_unfollowing_posts(self):
        """Тестирование отсутствия поста автора у нового пользователя."""
        new_user = User.objects.create(username='Lermontov')
        authorized_client = Client()
        authorized_client.force_login(new_user)
        response_unfollow = authorized_client.get(
            reverse('posts:follow_index')
        )
        context_unfollow = response_unfollow.context
        self.assertEqual(len(context_unfollow['page_obj']), 0)
