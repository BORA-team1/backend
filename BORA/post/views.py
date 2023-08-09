from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from post.models import Post,PostSec
from line.models import Line,Question
from .serializers import *
from vote.models import Vote
from django.db.models import Q
from vote.models import Vote
from debate.models import Debate

# Create your views here.

class SearchView(views.APIView):
    def get(self, request):
        # user = request.user
        keyword= request.GET.get('keyword')

        posts = (Post.objects.filter(title__icontains=keyword) | Post.objects.filter(hashtag__hashtag__icontains=keyword) | Post.objects.filter(post_user__nickname__icontains=keyword)).distinct()

        for post in posts:
            post.author=post.post_user.nickname
            if Vote.objects.filter(vote_post=post.post_id).exists():
                post.is_vote=True

            lines=Line.objects.filter(line_post=post.post_id).all()
            if Question.objects.filter(que_line__in=lines).exists():
                post.is_que=True
            if Debate.objects.filter(debate_line__in=lines).exists():
                post.is_debate=True

        serializer = PostSearchSerializer(posts, many=True)

        return Response({'message':'검색 성공', 'data': {"POST": serializer.data}}, status=status.HTTP_200_OK)

# class MainView(views.APIView):
#     def get(self, request):