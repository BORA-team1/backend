from rest_framework import serializers
from .models import Han, HanCom

class HanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Han
        fields = ['han_id', 'content', 'han_user', 'han_post', 'like']

class HanComSerializer(serializers.ModelSerializer):
    class Meta:
        model = HanCom
        fields = ['hancom_id', 'content', 'hancom_han', 'hancom_user']