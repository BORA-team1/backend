from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer,InterestSerializer
from audio.models import Playlist
from line.models import Line, LineCom, Question, Emotion
from vote.models import Vote, VotePer
from debate.models import Debate
from han.models import Han



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

class PostDetailSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    author=serializers.CharField(default=False)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','diff','author','date','hashtag']


class LineComPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineCom
        fields=['linecom_id']

class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields=['que_id']

class EmoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields=['emo_id','content']

class IngVotePostSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    class Meta:
        model = Vote
        fields=['vote_id','title','vote_user']

class DoneVotePostSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    result=serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields=['vote_id','title','item1', 'item2', 'item3', 'start_date','done_date','vote_user','result']
    def get_result(self, instance):
        result = {}  # 결과를 저장할 딕셔너리
        for age, _ in VotePer.AGES:
            for select, _ in VotePer.SELECTS:
                result[f"result{select}_{age}"] = VotePer.objects.filter(voteper_vote=instance, age=age, select=select).count()
        return result
    
class DebatePostSerializer(serializers.ModelSerializer):
    debate_user=UserProfileSerializer(many=True,source='debaters')
    class Meta:
        model = Debate
        fields = ['debate_id', 'title', 'cond','debate_user']

class LineSerializer(serializers.ModelSerializer):
    LineCom = LineComPostSerializer(many=True,source='linecom_line')
    Question = QuestionPostSerializer(many=True, source='que_line')
    Emotion = EmoPostSerializer(many=True, source='emo_line')
    IngVote=serializers.SerializerMethodField()
    DoneVote=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField()
    Debate=DebatePostSerializer(many=True, source='debate_line')
    
    class Meta:
        model = Line
        fields = ['line_id', 'sentence', 'content', 'is_my', 'LineCom', 'Question', 'Emotion', 'IngVote', 'DoneVote','Debate']

    def get_is_my(self, obj):
        request = self.context.get('request')
        if request.user in obj.line_user.all():
            return True
        else:
            return False
    
    def get_IngVote(self, obj):
        ing_votes = obj.vote_line.filter(is_done=False)
        serializer = IngVotePostSerializer(ing_votes, many=True)
        return serializer.data

    def get_DoneVote(self, obj):
        done_votes = obj.vote_line.filter(is_done=True)
        serializer = DoneVotePostSerializer(done_votes, many=True)
        return serializer.data


class PostSecSerializer(serializers.ModelSerializer):
    Lines=LineSerializer(many=True,source='line_postsec')
    class Meta:
        model=PostSec
        fields=['sec_id','num','title','content','Lines']
    def to_representation(self, instance):                  
        request = self.context.get('request')   
        representation = super().to_representation(instance)
        lines = instance.line_postsec.all().order_by('sentence')

        serializer = LineSerializer(lines, many=True, context={'request': request},source='line_postsec') 
        representation['Lines'] = serializer.data

        return representation
    

class HanSerializer(serializers.ModelSerializer):
    han_user=UserProfileSerializer()
    like_num=serializers.SerializerMethodField()
    do_like=serializers.SerializerMethodField()
    
    class Meta:
        model=Han
        fields=['han_id','content', 'do_like', 'like_num','han_user']

    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.que_user == request.user
        return False
    def get_do_like(self, obj):
        request = self.context.get('request')
        if request.user in obj.like.all():
            return True
        else:
            return False
    def get_like_num(self, obj):
        return obj.like.count()
    