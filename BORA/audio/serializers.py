from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from post.models import Post, PostSec
from mypage.serializers import InterestSerializer
from audio.models import Playlist,Audio
from account.serializers import InterestSerializer

class PostInAudioSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','post_user','title','diff','hashtag']

class PostSecInAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostSec
        fields=['sec_id','num','title','content']

# class AudioSecInAudioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=AudioSec
#         fields=['audiosec_id','num','audiofile']

class AudioDetailSerializer(serializers.ModelSerializer):
    audio_post=PostInAudioSerializer(read_only=True)
    class Meta:
        model=Audio
        fields=['audio_id','audio_post','audiofile']


class PostInAudioSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','title','diff','hashtag']

class AudioInPlaylistSerializer(serializers.ModelSerializer):
    audio_post=PostInAudioSerializer(read_only=True)
    class Meta:
        model=Audio
        fields=['audio_id','long','audio_post']

class PlaylistSerializer(serializers.ModelSerializer):
    playlist_audio=AudioInPlaylistSerializer(many=True, read_only=True)
    class Meta:
        model=Playlist
        fields=['playlist_id','title','playlist_audio']
    def get_playlist_audio(self, obj):
        sorted_audios = obj.playlist_audio.order_by('audio_id')
        serializer = AudioInPlaylistSerializer(sorted_audios, many=True, read_only=True)
        return serializer.data

class NewPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Playlist
        fields=['playlist_id','title','des','first_audio']
    
