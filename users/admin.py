from django.contrib import admin

from users.models import UserProfile, Friendship, FriendRequest


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "get_full_name", )


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass