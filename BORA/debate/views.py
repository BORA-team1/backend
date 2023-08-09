from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from audio.models import Playlist
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from django.db.models import Q

# Create your views here.
class IngDebateView(views.APIView):
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, cond__lt=3))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))
        lineseri=LineIngDebateSerializer(lines,many=True)
        return Response({"message": "진행중 투표 조회 성공", "data": {"Lines":lineseri.data}})


class DoneDebateView(views.APIView):
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, cond=3))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))     
        lineseri=LineDoneDebateSerializer(lines,many=True)
        return Response({"message": "완료된 투표 조회 성공", "data": {"Lines":lineseri.data}})

class MyDebateView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, debate_user=request.user.id))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))     
        lineseri=LineMyDebateSerializer(lines,many=True,context={'request': request})
        return Response({"message": "내가 만든 투표 조회 성공", "data": {"Lines":lineseri.data}})
