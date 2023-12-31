from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from audio.models import Playlist,Audio
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Create your views here.

class AudioDetailView(views.APIView):
    def get(self, request, audio_pk, playlist_pk):
        audio = get_object_or_404(Audio, audio_id=audio_pk)
        serializer = AudioDetailSerializer(audio)
        postsecs=PostSec.objects.filter(sec_post=audio.audio_post).all()
        postsecseri=PostSecInAudioSerializer(postsecs, many=True).data
        author_id=audio.audio_post.post_user.id
        # audiosecs=AudioSec.objects.filter(audiosec_audio=audio)
        # audiosecseri=AudioSecInAudioSerializer(audiosecs, many=True).data
        if request.user in audio.audio_post.bookmark.all():
            is_booked=True
        else:
            is_booked=False
        data={
            "audio_id":serializer.data['audio_id'],
            "author_id":author_id,
            "audio_post": serializer.data['audio_post'],
            "audiofile":serializer.data['audiofile'],
            "PostSec":postsecseri,
            # "AudioSec":audiosecseri
            "is_booked": is_booked
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
        # request에서 playlist_audio 삭제한 Request생성: 삭제 안하고 넘기면 Dict이 넘어왔다고 오류뜸
        # 오디오들: playlist_audio데이터 뽑아냄
        playlist_audioss = request.data.get('playlist_audio')
        playlist_audios = sorted(playlist_audioss, key=lambda x: x['audio_id'])

        # 첫번째 오디오: playlist_audio데이터의 첫번째 요소를 first_audio로 지정
        first_audio_id = playlist_audios[0]['audio_id']
        # first_audio=get_object_or_404(Audio,audio_id=first_audio_id)
       
        # Request에 담긴 데이터로 NewPlaylistSerializer생성
        serializer = NewPlaylistSerializer(data={
                            "title":request.data['title'],
                            "des":request.data['des'],
                            "first_audio":first_audio_id
                            })
        
        # 해시태그: 베이스 플레이리스트에서 hashtag뽑아와서 list로 저장
        base_pli=get_object_or_404(Playlist, playlist_id=request.data['playlist_id'])
        base_hashtag=list(base_pli.hashtag.all())
        
        if serializer.is_valid():
            # 작성자정보(mypli_user)와 첫번째오디오정보(first_audio)를 담아 시리얼라이저 save
            newpli=serializer.save(mypli_user = request.user)   

            # playlist_audios 필드에 오디오들 추가
            for audios in playlist_audios:
                audio=audios['audio_id']
                audioA= get_object_or_404(Audio,audio_id=audio)
                newpli.playlist_audio.add(audioA)
            
            # hashtag 필드에 해시태그 추가
            for ht in base_hashtag:
                newpli.hashtag.add(ht)
                          

            return Response({'message': '나만의 플리 성공', 'data': serializer.data, 'request':request.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class NextAudioView(views.APIView):
     def get(self, request, playlist_pk,audio_pk):
        try:
            playlist = Playlist.objects.get(pk=playlist_pk)
        except Playlist.DoesNotExist:
            return Response({'message': '플레이리스트가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        audio_set = playlist.playlist_audio.all()
        next_audio = audio_set.filter(Q(audio_id__gt=audio_pk)).order_by('audio_id').first()
        
        if next_audio:
            return Response({'audio': next_audio.audio_id}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '다음 오디오가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

