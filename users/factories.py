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

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    bio = Faker('paragraph', nb_sentences=3)
    birth_date = Faker('date_of_birth', minimum_age=18, maximum_age=80)
    is_active = True
    is_staff = False
    date_joined = LazyAttribute(lambda o: timezone.now())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use create_user for correct user creation"""
        manager = cls._get_manager(model_class)
        
        # Extract email and password from kwargs
        email = kwargs.pop('email', None)
        password = kwargs.pop('password', 'password123')  # Default password if not provided
        
        # If email is not provided, generate one
        if not email:
            email = cls.email.evaluate(None, None, extra=kwargs)
        
        # Create the user using the custom create_user method
        return manager.create_user(email=email, password=password, **kwargs)

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        """
        Do not set password here as it's already set in create_user.
        This method is kept for backwards compatibility with existing tests.
        """
        pass
    

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