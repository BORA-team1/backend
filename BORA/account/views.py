from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class SignUpView(views.APIView):
    def post(self,request):
        hashtags = request.data.get('interest')

        Request=request.data.copy()
        Request.pop('interest')

        serializer=SignUpSerializer(data=Request)
        if serializer.is_valid():


            user=serializer.save()                          # 회원가입
            # 해시태그(관심사) 추가

            hashtags_list = hashtags.split()
            hashtags_list_end = [tag[1:] for tag in hashtags_list if tag.startswith('#')]
            print(hashtags_list_end)
            for tag in hashtags_list_end:
                print(tag)
                hashtag , _ = Hashtag.objects.get_or_create(hashtag=tag)
                user.interest.add(hashtag)
            return Response({'message':'회원가입 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'회원가입 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message': "로그인 실패", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       

class MyProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'message': '프로필 가져오기 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
    

#아이디 중복 확인
class DuplicateIDView(views.APIView):
    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            response_data = {'duplicate':True}
        else:
            response_data = {'duplicate':False}
        
        return Response(response_data, status=status.HTTP_200_OK)
