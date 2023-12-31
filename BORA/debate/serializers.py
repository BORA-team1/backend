from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer


class DebateSerializer(serializers.ModelSerializer):
    debate_user=UserProfileSerializer()
    is_my=serializers.SerializerMethodField()
    class Meta :
        model=Debate
        fields=['debate_id','title', 'cond','link', 'debate_user', 'is_my']
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.debate_user == request.user
        return False
    
class LineIngDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,cond=1).all()
        return DebateSerializer(debates, many=True, context={'request': request}).data
    
class LineDoneDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,cond=2).all()
        return DebateSerializer(debates, many=True,context={'request': request}).data
    
class LineMyDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,debate_user=request.user.id).all()
        return DebateSerializer(debates, many=True,context={'request': request}).data
    
class NewDebateSerializer(serializers.ModelSerializer):
    class Meta :
        model=Debate
        fields=['debate_id','title','cond','debate_user','debate_postsec','debate_line','link']