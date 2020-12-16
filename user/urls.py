from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('', dashboard, name='dashboard'),
    path('logout/', logout, name='logout')
]
