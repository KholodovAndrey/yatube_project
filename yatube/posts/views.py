# posts/views.py
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    posts = Post.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context) 


def group_list(request):
    template = 'posts/group_list.html'
    text = "Здесь будет информация о группах проекта Yatube"
    context = {
        'text': text,
    }
    return render(request, template, context)


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
