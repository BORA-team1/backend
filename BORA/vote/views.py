from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.


class VoteCreateView(views.APIView):
    #투표 등록
    def post(self, request):
        data = request.data.copy()
        data['vote_user'] = request.user.id #현재 로그인한 사용자를 투표 작성자로 설정
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class VoteView(views.APIView):
    #투표하기
    def post(self, request, vote_id):
        try:
            vote = Vote.objects.get(pk=vote_id)
        except Vote.DoesNotExist:
            return Response({'message': '투표가 존재하지 않습니다.'}, status=HTTP_404_NOT_FOUND)

        selected_item = request.data.get('selected_item')  # 클라이언트가 선택한 항목
        age = request.data.get('age')  # 사용자 연령대
        user = request.user

        if selected_item not in [vote.item1, vote.item2, vote.item3]:
            return Response({'message': '유효하지 않은 항목입니다.'}, status=HTTP_400_BAD_REQUEST)

        # 투표 결과 저장
        vote_per = VotePer.objects.create(
            age=age,
            select=selected_item,
            voteper_vote=vote,
            voteper_user=user
        )

        return Response({'message': '투표 완료', 'data': VotePerSerializer(vote_per).data}, status=HTTP_201_CREATED)

class VoteIngView(generics.ListAPIView):
    #진행중인 투표 조회
    serializer_class = VoteSerializer

    def get_queryset(self):
        return Vote.objects.filter(is_done=False)
    
class DoneVoteView(generics.RetrieveAPIView):
    #완료된 투표 조회
    serializer_class = DoneVoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Vote.objects.filter(is_done=True, vote_per_vote__voteper_user=user)
    