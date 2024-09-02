from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.managers import UserProfileManager

class UserProfile(AbstractUser):
    # Add any additional fields you need for your user model
    username = None
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserProfileManager()
    
    def __str__(self):
        return self.email
    
    def get_friends(self):
        return self.friends.filter(status=Friendship.ACCEPTED)

    def get_pending_friend_requests(self):
        return FriendRequest.objects.filter(to_user=self, status=FriendRequest.PENDING)

class Friendship(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(UserProfile, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} - {self.friend} ({self.get_status_display()})"

class FriendRequest(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    from_user = models.ForeignKey(UserProfile, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} to {self.to_user} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only check on creation
            recent_requests = FriendRequest.objects.filter(
                from_user=self.from_user,
                created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
            ).count()
            if recent_requests >= 3:
                raise ValidationError("You can't send more than 3 friend requests within a minute.")
        super().save(*args, **kwargs)

    def accept(self):
        if self.status == self.PENDING:
            self.status = self.ACCEPTED
            self.save()
            Friendship.objects.create(user=self.from_user, friend=self.to_user, status=Friendship.ACCEPTED)
            Friendship.objects.create(user=self.to_user, friend=self.from_user, status=Friendship.ACCEPTED)

    def reject(self):
        if self.status == self.PENDING:
            self.status = self.REJECTED
            self.save()