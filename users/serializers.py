from django.contrib.auth.models import Group, User
from rest_framework import serializers, validators
from django.utils.translation import gettext_lazy as _

from users.models import UserProfile, Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "email", "password", "first_name", "last_name", "date_joined", "birth_date"]

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'friend'),
                message=_("Friend request already exsits.")
            )
        ]