from django.contrib.auth.models import Group, User
from rest_framework import serializers

from users.models import UserProfile, FriendRequest, Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "email", "first_name", "last_name", "date_joined", "birth_date"]
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'
