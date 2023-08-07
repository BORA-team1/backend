from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from post.models import Post,PostSec
from line.models import Line
from .serializers import *


# Create your views here.

class MyLineView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user
        lines= Line.objects.filter(line_post=post).all()
        mylines= lines.filter(line_user=now_user).all()
        mylineseri=MyLineSerializer(mylines, many=True)
        return Response({'message': '내 밑줄 전체 조회 성공', 'data': {'Lines':mylineseri.data}}, status=status.HTTP_200_OK)
    
    def post(self, request, post_pk):
        now_user=request.user
        post= get_object_or_404(Post, post_id=post_pk)                                 # 현재 포스트 객체
        post_sec=get_object_or_404(PostSec, sec_id=request.data['line_postsec'])       # 현재 포스트 섹션
        sentence=request.data['sentence']   
        line, created = Line.objects.get_or_create(line_post=post,line_postsec=post_sec,sentence=sentence)            # 현재 포스트의 섹션의 순번에 해당하는 line이 있으면 가져오고 없으면 만든다. 만들어졌다면 created=true
        line.line_user.add(now_user)                                                   # 현재 사용자 추가
        return Response({'message': '밑줄 긋기 성공', 'data': {'line_id': line.line_id, 'sentence': line.sentence}}, status=status.HTTP_200_OK)
   
class MyLineComView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        linecoms1= LineCom.objects.filter(linecom_user=now_user).all()            # 사용자가 쓴 모든 LineCom
        linecoms= linecoms1.filter(linecom_line__line_post=post).all()            # 사용자의 LineCom중 현재 Post에 있는것만
        
        Lines=list(set([linecom.linecom_line for linecom in linecoms]))                      # 사용자의 LineCom이 있는 Line만

        seri=MyLineandComSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 댓글 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineQnAView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        que= Question.objects.filter(que_user=now_user).all()            
        questions= que.filter(que_line__line_post=post).all()           
        
        Lines=list(set([question.que_line for question in questions]))

        seri=MyLineandQueSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 Q&A 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineEmoView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        emo= Emotion.objects.filter(emo_user=now_user).all()            
        emotions= emo.filter(emo_line__line_post=post).all()           
        
        Lines=list(set([emotion.emo_line for emotion in emotions]))

        seri=MyLineandEmoSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 감정표현 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        line.line_user.remove(request.user)
        return Response({"message": "내 밑줄 삭제 성공"})


class LineComView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, line_pk):
        line= get_object_or_404(Line, line_id=line_pk)
        linecoms=LineCom.objects.filter(linecom_line=line).all()
        serializer=LineComSerializer(linecoms,context={'request': request},many=True)
        return Response({'message': '밑줄 댓글 조회 성공', 'data': {'line_id':line.line_id,'content':line.content,'LineCom':serializer.data}}, status=status.HTTP_200_OK)

    def post(self, request, line_pk):
        line= get_object_or_404(Line, line_id=line_pk)
        now_user=request.user
        postsec=line.line_postsec
        serializer = NewLineComSerializer(data={
                    'content': request.data['content'],
                    'linecom_line': line_pk,
                    'linecom_postsec': postsec.sec_id,
                    'linecom_user': now_user.id
                })
        if serializer.is_valid():
            serializer.save()   
            return Response({'message':'밑줄 댓글 등록 성공','data':{'linecom_line':serializer.data['linecom_line'],'linecom_id':serializer.data['linecom_id'],'linecom_user':serializer.data['linecom_user'],"content":serializer.data['content']}}, status=status.HTTP_201_CREATED)
        return Response({'message':'밑줄 댓글 등록 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class DeleteComView(views.APIView):
    def delete(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.delete()
        return Response({"message": "밑줄 댓글 삭제 성공"})

class LineComLikeView(views.APIView):
    def post(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.like.add(request.user)
        serializer=LineComLikeSerializer(linecom,context={'request': request})
        return Response({"message": "밑줄 댓글 좋아요 성공","data":serializer.data})
    def delete(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.like.remove(request.user)
        serializer=LineComLikeSerializer(linecom,context={'request': request})
        return Response({"message": "밑줄 댓글 좋아요 취소 성공","data":serializer.data})

