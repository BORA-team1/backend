from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import logout

# Create your views here.
class SignUpView(views.APIView):
    def post(self,request):
        serializer=SignUpSerializer(data=request.data)     # 입력받은 댓글 데이터를 시리얼라이저에 넣어 변환
        # hashtag=request.interest
        # for tag in hashtag:
        #     new_hashtag=Hashtag.objects.get_or_create(hashtag=tag)
        #     new_hashtag.add(Hashtag)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공','data':serializer.data})
        return Response({'message':'회원가입 실패','error':serializer.errors})
    

        # hashtags=request.POST['hashtags']
        # hashtag=hashtags.split(",")
        # for tag in hashtag:
        #     # new_hashtag=HashTag()
        #     # new_hashtag.hashtag=tag
        #     # new_hashtag.save()
        #     # new_blog.hashtag.add(new_hashtag)
        #     new_hashtag=HashTag.objects.get_or_create(hashtag=tag)
        #     new_blog.hashtag.add(new_hashtag[0])
        # return redirect ('detail',new_blog.id)




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
       