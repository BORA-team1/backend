from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer,InterestSerializer



class PostSearchSerializer(serializers.ModelSerializer):
    is_vote = serializers.BooleanField(default=False)
    is_debate = serializers.BooleanField(default=False)
    is_que = serializers.BooleanField(default=False)
    hashtag=InterestSerializer(many=True, read_only=True)
    author=serializers.CharField()
    class Meta:
        model=Post
        fields=['post_id','title','post_image','hashtag', 'author', 'is_vote' ,'is_debate','is_que']