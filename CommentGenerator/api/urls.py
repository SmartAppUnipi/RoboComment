from django.urls import path

from . import views

urlpatterns = [
    path('action/', views.action, name='index'),
]
