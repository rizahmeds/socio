from django.contrib import admin

from users.models import UserProfile, Friendship, FriendRequest


@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = ("email", "username", "get_full_name", )


@admin.register(Friendship)
class AdminFriendship(admin.ModelAdmin):
    pass


@admin.register(FriendRequest)
class AdminFriendRequest(admin.ModelAdmin):
    pass