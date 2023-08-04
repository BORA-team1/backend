from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status

# Create your views here.
class SignUpView(views.APIView):
    def post(self,request):
        serializer=SignUpSerializer(data=request.data)  
        if serializer.is_valid():
            user=serializer.save()                          # 회원가입
            # 해시태그(관심사) 추가
            hashtags = request.data.get('interest', [])     # interest 받아옴
            for hashtag_name in hashtags:                   # 리스트 쪼갬
                tag=hashtag_name['hashtag']                 # hashtag 키의 값
                hashtag, _ = Hashtag.objects.get_or_create(hashtag=tag)  # 해당 이름을 가진 Hashtag 인스턴스를 데이터베이스에서 찾거나 없으면 생성
                user.interest.add(hashtag)                               # User 모델의 interest에 해당 Hashtag 인스턴스를 추가
            return Response({'message':'회원가입 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'회원가입 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(views.APIView):
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)       # 입력받은 댓글 데이터를 시리얼라이저에 넣어 변환
        if serializer.is_valid():                               # 로그인이라 save는 안해도됨
            return Response({'message':'로그인 성공','data':serializer.data})
        return Response({'message':'로그인 실패','error':serializer.errors})
    

class LogoutView(views.APIView):
    def delete(self,request):
        user = request.user
        logout(request)
        return Response({'message':'로그아웃 성공'})
       