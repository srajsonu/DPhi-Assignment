from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.signin, name='signin'),

    path('index/', views.index, name='index'),
    path('signup/<int:user>/', views.signup_type, name='signup_type'),
    path('signup/post/<int:user>/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.signout, name='logout')
]
