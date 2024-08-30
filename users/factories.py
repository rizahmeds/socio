import factory
from factory.django import DjangoModelFactory
from factory import Faker, LazyAttribute, SubFactory
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

from users.models import UserProfile, Friendship, FriendRequest

User = get_user_model()


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_active = True
    is_staff = False
    date_joined = Faker('date_time_this_decade', tzinfo=None)
    
    # Custom fields we added to the User model
    bio = Faker('paragraph', nb_sentences=3)
    birth_date = Faker('date_of_birth', minimum_age=18, maximum_age=80)

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        self.set_password(extracted if extracted else 'password123')

    @factory.post_generation
    def friends(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for friend in extracted:
                self.friends.add(friend)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use create_user for correct password hashing"""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
    

class FriendRequestFactory(DjangoModelFactory):
    class Meta:
        model = FriendRequest

    from_user = SubFactory(UserProfileFactory)
    to_user = SubFactory(UserProfileFactory)
    status = FriendRequest.PENDING
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to ensure from_user and to_user are different"""
        obj = super()._create(model_class, *args, **kwargs)
        while obj.from_user == obj.to_user:
            obj.to_user = UserProfileFactory()
        obj.save()
        return obj


class FriendshipFactory(DjangoModelFactory):
    class Meta:
        model = Friendship

    user = SubFactory(UserProfileFactory)
    friend = SubFactory(UserProfileFactory)
    status = Friendship.ACCEPTED
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to ensure user and friend are different"""
        obj = super()._create(model_class, *args, **kwargs)
        while obj.user == obj.friend:
            obj.friend = UserProfileFactory()
        obj.save()
        return obj