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
import random
from django.db.models import Count, F
from audio.models import Audio
from account.models import User

# Create your views here.

class SearchView(views.APIView):
    def get(self, request):
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

class MainView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        # 랜덤 추천
        all_posts = Post.objects.all()
        random_posts = random.sample(list(all_posts), 5)
        for randompost in random_posts:
            if randompost.bookmark.filter(pk=user.id).exists():
                randompost.is_booked=True
        random_posts_seri = PostBoxSerializer(random_posts,many=True)

        # 난이도 하
        lights = Post.objects.filter(diff=1).all()[:4]
        for post in lights:
            post.author=post.post_user.nickname
            if Vote.objects.filter(vote_post=post.post_id).exists():
                post.is_vote=True
            lines=Line.objects.filter(line_post=post.post_id).all()
            if Question.objects.filter(que_line__in=lines).exists():
                post.is_que=True
            if Debate.objects.filter(debate_line__in=lines).exists():
                post.is_debate=True
        lightseri = PostSearchSerializer(lights, many=True)

        # 난이도 중
        medis = Post.objects.filter(diff=2).all()[:4]
        for post in medis:
            post.author=post.post_user.nickname
            if Vote.objects.filter(vote_post=post.post_id).exists():
                post.is_vote=True
            lines=Line.objects.filter(line_post=post.post_id).all()
            if Question.objects.filter(que_line__in=lines).exists():
                post.is_que=True
            if Debate.objects.filter(debate_line__in=lines).exists():
                post.is_debate=True
        mediseri = PostSearchSerializer(medis, many=True)

        # 난이도 하
        heavys = Post.objects.filter(diff=3).all()[:4]
        for post in heavys:
            post.author=post.post_user.nickname
            if Vote.objects.filter(vote_post=post.post_id).exists():
                post.is_vote=True
            lines=Line.objects.filter(line_post=post.post_id).all()
            if Question.objects.filter(que_line__in=lines).exists():
                post.is_que=True
            if Debate.objects.filter(debate_line__in=lines).exists():
                post.is_debate=True
        heavyseri = PostSearchSerializer(heavys, many=True)

        # 랜덤 나이대
        # random_age = random.randint(1, 5)
        random_age =4 # 40대로 고정
        print(random_age)

        # ??나이대가 가장 많이 밑줄그은 Line
        most_liked_post_by_age = Line.objects.annotate(
            age_like_count=Count('line_user', filter=Q(line_user__age=random_age))
        ).order_by('-age_like_count').first()

        hotline_content=most_liked_post_by_age.content
        hotline_author=most_liked_post_by_age.line_post.post_user.nickname
        hotline_post=most_liked_post_by_age.line_post

        HotPost=PostBoxSerializer(hotline_post)

        # 모든 플레이리스트
        playlists=Playlist.objects.filter(is_base=True).all()
        PlaylistSeri=PliSerializer(playlists,many=True)

        data={
            "Random":random_posts_seri.data,
            "PostLight":lightseri.data,
            "PostMed":mediseri.data,
            "PostHeavy":heavyseri.data,
            "HotLine":{
                "content": hotline_content,
                "author": hotline_author
            },
            "HotPost": HotPost.data,
            "PlayList": PlaylistSeri.data

        }
        return Response({'message':'보는 아티클 홈 조회 성공', 'data': data}, status=status.HTTP_200_OK)

class PostListView(views.APIView):
    def get(self, request):
        all_posts = Post.objects.all()
        for post in all_posts:
            post.author=post.post_user.nickname
            if Vote.objects.filter(vote_post=post.post_id).exists():
                post.is_vote=True
            lines=Line.objects.filter(line_post=post.post_id).all()
            if Question.objects.filter(que_line__in=lines).exists():
                post.is_que=True
            if Debate.objects.filter(debate_line__in=lines).exists():
                post.is_debate=True
        postlistseri = PostSearchSerializer(all_posts, many=True)

        count=all_posts.count()
        data={
            "count":count,
            "Post": postlistseri.data
        }

        return Response({'message':'보는 아티클 전체 조회 성공', 'data': data}, status=status.HTTP_200_OK)