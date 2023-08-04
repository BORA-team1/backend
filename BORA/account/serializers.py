from rest_framework import serializers
from .models import *
from collections import OrderedDict


# class InterestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hashtag
#         fields = ["hashtag"]


class SignUpSerializer(serializers.ModelSerializer):            # 유저 시리얼라이저
    class Meta:
        model=User
        fields=['user_id','username','password','nickname','profile','gender','age']
    def create(self, validated_data):                # 회원정보가 save될 때 원래 create가 쓰일것임 그때 set_password라는 기능을 추가한 느낌
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            profile=validated_data['profile'],
            gender=validated_data['gender'],
            age=validated_data['age']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128,write_only=True)

    def validate(self, data):
        username = data.get("username",None)
        password = data.get("password",None)

        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username)

            if not user.check_password(password):
                raise serializers.ValidationError()
            else:
                return user