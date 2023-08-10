from rest_framework import serializers
from .models import *
from account.serializers import UserProfileSerializer

class VoteSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    class Meta:
        model = Vote
        fields = ['vote_id', 'title', 'item1', 'item2', 'item3', 'is_done', 'start_date', 'done_date', 'vote_post', 'vote_line', 'vote_postsec', 'vote_user']

class VotePerSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    class Meta:
        model = Vote
        fields = ['voteper_id', 'age', 'select', 'voteper_vote', 'voteper_user']


class DoneVoteSerializer(serializers.ModelSerializer):
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
