from django.db import transaction
from django.core.management.base import BaseCommand

from users.factories import (
    FriendRequestFactory,
    FriendshipFactory,
    UserProfileFactory,
)
from users.models import UserProfile, Friendship, FriendRequest

NUM_USERS = 50


class Command(BaseCommand):
    help = "Generates test data for users..."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [UserProfile, Friendship, FriendRequest]
        for m in models:
            if isinstance(m, UserProfile):
                m.objects.exclude(is_superuser=True).delete()
            m.objects.exclude().delete()

        self.stdout.write("Creating new data...")
        # Create dummy users
        for _ in range(NUM_USERS):
            UserProfileFactory()
            FriendshipFactory()
            FriendRequestFactory()


        
