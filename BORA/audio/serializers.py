from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from post.models import Post, PostSec
from mypage.serializers import InterestSerializer

class PostInAudioSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','post_user','title','diff','hashtag']

class PostSecInAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostSec
        fields=['sec_id','num','title','content']

class AudioSecInAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model=AudioSec
        fields=['audiosec_id','num','audiofile']

class AudioDetailSerializer(serializers.ModelSerializer):
    audio_post=PostInAudioSerializer(read_only=True)
    class Meta:
        model=Audio
        fields=['audio_id','audio_post']
