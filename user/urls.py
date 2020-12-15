from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('signin/', signin, 'signin'),
    path('signup/', signup, 'signup')
]
