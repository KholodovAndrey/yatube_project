# posts/views.py
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    return render(request, template)


def group_list(request):
    template = 'posts/group_list.html'
    return render(request, template)


# Страница со списком постов
def posts_list(request):
    return HttpResponse('Список постов')


# Страница с постами от группы
def group_posts(request, pk):
    return HttpResponse(f'Посты, отсортированные по группам {pk}')


# Страница с иодним постом;
# view-функция принимает параметр pk из path()
def posts_detail(request, pk):
    return HttpResponse(f'Пост номер {pk}') 
