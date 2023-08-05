from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import *

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