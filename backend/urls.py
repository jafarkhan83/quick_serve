from django.urls import path
from backend import views

urlpatterns = [
    path('hello', views.hello),
    path('register', views.register),
    path('login', views.login),
]
