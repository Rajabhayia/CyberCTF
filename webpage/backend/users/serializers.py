# users/serializers.py
from rest_framework import serializers

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    points = serializers.IntegerField()
    team = serializers.CharField(max_length=150)
    message = serializers.CharField(required=False)

class TeamSerializer(serializers.Serializer):
    TeamName = serializers.CharField(max_length=150)
    leaderName = serializers.CharField(max_length=150)
    points = serializers.IntegerField()
    members = serializers.CharField(required=False)
    request = serializers.CharField(required=False)