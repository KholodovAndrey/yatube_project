from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()
POSTS_AMOUNT_SYMBOLS = 15
COMMENT_AMOUNT_SYMBOLS = 15


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Group name')
    slug = models.SlugField(unique=True, verbose_name='Group tag')
    description = models.TextField(verbose_name='Group description')

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:POSTS_AMOUNT_SYMBOLS]

    class Meta:
        ordering = ['-pub_date']


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст вашего комментария'
    )

    def __str__(self):
        return self.text[:COMMENT_AMOUNT_SYMBOLS]

    class Meta:
        ordering = ['-pub_date']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    constrains = [
        models.UniqueConstraint(
            fields=['user', 'author'], name='unique_following'
        )
    ]
