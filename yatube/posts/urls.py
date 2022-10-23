# yatube/posts/urls.py
# Эта строчка обязательна. 
# Без неё namespace работать не будет:
# namespace должен быть объявлен при include и тут, в app_name
app_name = 'posts'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('group_list/', views.group_list, name = 'group_list')
]
