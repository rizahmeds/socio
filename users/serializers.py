from django.contrib.auth.models import Group, User
from rest_framework import serializers

from users.models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined", "birth_date"]
