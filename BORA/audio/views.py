from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from audio.models import Playlist
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class AudioDetailView(views.APIView):
    def get(self, request, audio_pk, playlist_pk):
        audio = get_object_or_404(Audio, audio_id=audio_pk)
        serializer = AudioDetailSerializer(audio)
        postsecs=PostSec.objects.filter(sec_post=audio.audio_post).all()
        postsecseri=PostSecInAudioSerializer(postsecs, many=True).data
        audiosecs=AudioSec.objects.filter(audiosec_audio=audio)
        audiosecseri=AudioSecInAudioSerializer(audiosecs, many=True).data
        data={
            "audio_id":serializer.data['audio_id'],
            "audio_post": serializer.data['audio_post'],
            "PostSec":postsecseri,
            "AudioSec":audiosecseri
        }
        return Response({'message': '오디오북 상세 조회 성공', 'data': data}, status=status.HTTP_200_OK)
    

class PlaylistView(views.APIView):
     def get(self, request, playlist_pk):
        playlist = get_object_or_404(Playlist, playlist_id=playlist_pk)
        serializer=PlaylistSerializer(playlist)
        return Response({'message': '플레이리스트 조회 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
     
class NewPlaylistView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Request=request.data.copy()
        Request.pop('playlist_audio')    
        playlist_audios=request.data['playlist_audio']

        first_audio_id = playlist_audios[0]['audio_id']
        first_audio=get_object_or_404(Audio,audio_id=first_audio_id)
        # for audios in playlist_audios:
        #     audio=audios['audio_id']
        #     audioA, _ = Audio.objects.get_or_create(hashtag=audio)
        #     serializer.playlist_audio.add(audioA)
        serializer = NewPlaylistSerializer(data=Request)
        
        # for audios in playlist_audio:
        #     serializer.playlist_audio.add(playlist_audio)
        # now_user=request.user
        base_pli=get_object_or_404(Playlist, playlist_id=request.data['playlist_id'])
        base_hashtag=list(base_pli.hashtag.all())

       
        serializer.first_audio= get_object_or_404(Audio, audio_id=request.data['playlist_audio'][0]['audio_id'])
        serializer.hashtag=base_hashtag
        # serializer.mypli_user=now_user
        
        if serializer.is_valid():
            # serializer.mypli_user = request.user

            newpli=serializer.save(mypli_user = request.user,first_audio=first_audio)

            # serializer.validated_data['mypli_user'] = request.user
            # serializer.validated_data['']
            for audios in playlist_audios:
                audio=audios['audio_id']
                audioA, _ = Audio.objects.get_or_create(audio_id=audio)
                newpli.playlist_audio.add(audioA)
            

            for ht in base_hashtag:
                newpli.hashtag.add(ht)
            


            # hashtags = request.data.get('interest', [])     # interest 받아옴
            # for hashtag_name in hashtags:                   # 리스트 쪼갬
            #     tag=hashtag_name['hashtag']                 # hashtag 키의 값
            #     hashtag, _ = Hashtag.objects.get_or_create(hashtag=tag)  # 해당 이름을 가진 Hashtag 인스턴스를 데이터베이스에서 찾거나 없으면 생성
            #     user.interest.add(hashtag)                 

            return Response({'message': '나만의 플리 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors)





# class Playlist(models.Model):
#     playlist_id=models.AutoField(primary_key=True)
#     # title=models.CharField(max_length=200)
#     # des=models.CharField(max_length=400,null=True,blank=True)
#     is_base=models.BooleanField(default=False)
#     first_audio=models.ForeignKey(Audio,related_name='first_audio',on_delete=models.SET_NULL,null=True)
#     playlist_audio=models.ManyToManyField(Audio,related_name='playlist_audio')
#     hashtag=models.ManyToManyField(Hashtag)
#     mypli_user=models.ForeignKey(User, related_name='mypli_user',on_delete=models.CASCADE)


# def post(self, request):
#         serializer = self.NoticeSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response({'message': 'TF 공지 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
#         else:
#             return Response({'message': 'TF 공지 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
#  def post(self, request, pk):
#         booth = get_object_or_404(Booth, pk=pk)
#         serializer = self.CommentSerializer(data=request.data)
        
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user, booth=booth)
#             return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
#         else:
#             return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
# {
# 	"title": "[제목]",
# 	"des": "[추가 설명]",
# 	"playlist_id": 2,                  # 기존 플레이리스트 id
# 	"playlist_audio": [
# 			{ "audio_id": 1 },
# 			{ "audio_id": 12 },
# 			{ "audio_id": 130 }
# 	]
# }