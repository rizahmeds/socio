from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import filters

from users.models import FriendRequest, UserProfile, Friendship
from users.serializers import FriendshipSerializer, UserSerializer, FriendRequestSerializer
from users.throttling import FriendRequestRateThrottle


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    search_fields = ['email', 'first_name', 'last_name']


class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows friend requests to be viewed or edited.
    """
    queryset = FriendRequest.objects.all().order_by('-created_at')
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]

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

class SignupView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print("user: ", user, username, password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        