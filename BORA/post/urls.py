from django.contrib import admin
from django.urls import path
from .views import *

app_name='post'      

urlpatterns = [
    path('search/',SearchView.as_view()),
    # path('',MainView.as_view())
]