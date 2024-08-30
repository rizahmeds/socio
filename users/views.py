from rest_framework import permissions, viewsets

from users.models import FriendRequest, UserProfile, Friendship
from users.serializers import FriendshipSerializer, UserSerializer, FriendRequestSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows friend requests to be viewed or edited.
    """
    queryset = FriendRequest.objects.all().order_by('-created_at')
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = self.queryset.filter(status=status)
        return queryset


class FriendshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows list friends.
    """
    queryset = Friendship.objects.all().order_by('-created_at')
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]