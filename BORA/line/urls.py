from django.contrib import admin
from django.urls import path
from .views import *

app_name='line'      

urlpatterns = [
        path('<int:post_pk>/',MyLineView.as_view()),
        path('<int:post_pk>/com/',MyLineComView.as_view()),
        path('<int:post_pk>/qna/',MyLineQnAView.as_view()),
        path('<int:post_pk>/emo/',MyLineEmoView.as_view()),
        path('delete/<int:line_pk>/',MyLineDelete.as_view()),
]