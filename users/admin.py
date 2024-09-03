from django.contrib import admin

from users.models import UserProfile, Friendship


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "get_full_name",)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("user", "friend", "status")
