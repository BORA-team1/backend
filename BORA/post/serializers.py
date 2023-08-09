from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer,InterestSerializer
from audio.models import Playlist



class PostSearchSerializer(serializers.ModelSerializer):
    is_vote = serializers.BooleanField(default=False)
    is_debate = serializers.BooleanField(default=False)
    is_que = serializers.BooleanField(default=False)
    hashtag=InterestSerializer(many=True, read_only=True)
    author=serializers.CharField(default=False)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','hashtag', 'author', 'is_vote' ,'is_debate','is_que']

class PostBoxSerializer(serializers.ModelSerializer):
    is_booked = serializers.BooleanField(default=False)
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','diff','is_booked','hashtag']

class PliSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Playlist
        fields=['playlist_id','title','hashtag','first_audio']
