# posts/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Post, Group


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    template = 'posts/index.html'
    title = 'Главная страница'
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts
    }
    template = 'posts/group_list.html'

    return render(request, template, context)


def posts_list(request):
    return HttpResponse('Список постов')


def posts_detail(request, pk):
    return HttpResponse(f'Пост номер {pk}')
