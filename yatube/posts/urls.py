from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('group_list/', views.group_list)
]
