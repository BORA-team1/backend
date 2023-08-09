from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
# Create your views here.

#한마디 조회/작성/삭제
class HanView(views.APIView):
    serializer_class = HanSerializer
    permission_classes = [IsAuthenticated] 
    #한마디 조회
    def get(self, request, han_id):                     
        han=get_object_or_404(Han, pk=han_id)
        serializer = HanSerializer(Han, many=True)     
        return Response({'message': '한마디 조회 성공', 'data': {'han': han.data}}, status=HTTP_200_OK)
    #한마디 등록
    def post(self, request, pk):
        data = {
            'han_id' : pk,
            'han_user' : request.user.id,
            'content' : request.data.get('content')
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '한마디 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '한마디 작성 실패', 'data': serializer.error}, status=HTTP_400_BAD_REQUEST)
    #한마디 삭제
    def delete(self, request, pk):
        han_id = request.data.get('han_id')
        han = get_object_or_404(Han, pk = han_id)
        han.delete()

        return Response({'message' : '한마디 삭제 성공'}, status=HTTP_204_NO_CONTENT)


#한마디 추천 관련 view
class HanRecommendView(views.APIView):
    serializer_class = HanSerializer
    permission_classes = [IsAuthenticated] 
    #한마디 추천
    def post(self, request, pk):
        han_user = request.user
        han = get_object_or_404(Han, pk=pk) #han_post가 맞나
        han.like.add(han_user) #좋아요 취소가 가능하니 유저 정보 넘겨줘야겠지?
        han.is_liked = True

        serializer = self.serializer_class(data=request.data, instance=han, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '한마디 추천 성공', 'data': {'han': serializer.data['id'], 'is_liked': serializer.data['is_liked']}}, status=HTTP_200_OK)
        else:
            return Response({'message': '한마디 추천 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    #한마디 추천 취소
    def delete(self, request, pk):
        han_user = request.user #한마디 추천과 동일
        han = get_object_or_404(Han, pk=pk) 
        han.like.remove(han_user)
        han.is_liked = False

        serializer = self.serializer_class(data=request.data, instance=han, partial=True)     

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '한마디 추천 취소 성공', 'data': {'han': serializer.data['id'], 'is_liked': serializer.data['is_liked']}}, status=HTTP_200_OK)
        else:
            return Response({'message': '한마디 추천 취소 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

#한마디 답글
class HanComView(views.APIView):
    serializer_class = HanComSerializer
    permission_classes = [IsAuthenticated] 
    #한마디 답글 달기
    def post(self, request, pk):
        hancom=get_object_or_404(HanCom, hancom_id=pk)
        hancomcom=HanComSerializer(data={'content':request.data['content'],'hancom_user':request.user.id})
        if hancomcom.is_valid():
            hancomcom.save(linecomcom_lineCom=hancom)   # 시리얼라이저 필드에 없는 값 추가
            return Response({'message':'한마디 답글 작성 성공','data':hancomcom.data}, status=HTTP_200_OK)
        return Response({'message':'한마디 답글 작성 실패','error':hancomcom.errors},status=HTTP_400_BAD_REQUEST)
    #한마디 답글 삭제
    def delete(self, request, pk):
        hancomcom=get_object_or_404(HanCom,hancomcom_id=pk)
        hancomcom.delete()
        return Response({"message": " 한마디 답글 삭제 성공"})