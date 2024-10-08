from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import filters

from users.models import UserProfile, Friendship
from users.serializers import FriendshipSerializer, UserSerializer
from users.throttling import FriendRequestRateThrottle
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    search_fields = ['email', 'first_name', 'last_name']

    def get_queryset(self):
        queryset = self.queryset.exclude(id=self.request.user.id)
        return queryset


class FriendshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows list friends.
    """
    queryset = Friendship.objects.all().order_by('-created_at')
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]
    lookup_field = 'pk'

    def get_queryset(self):
        # list of users who have accepted friend request
        queryset = self.queryset.filter(user=self.request.user.id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_throttles(self):
        """
        Override the default throttles to exclude them for accept and reject actions.
        """
        if self.action in ['accept', 'reject']:
            return []  # No throttles for accept and reject actions
        return super().get_throttles()
    
    @action(detail=True, methods=['PUT'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.status == 'A':
            return Response({
                'error': 'Friend request already accepted.'
            }, status=status.HTTP_400_BAD_REQUEST)
        friendship.status = 'A'
        friendship.save()
        return Response({
            'message': 'Friend request accepted successfully.'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT'])
    def reject(self, request, pk=None):
        friendship = self.get_object()
        if friendship.status == 'R':
            return Response({
                'error': 'Friend request already rejected.'
            }, status=status.HTTP_400_BAD_REQUEST)
        friendship.status = 'R'
        friendship.save()
        return Response({
            'message': 'Friend request rejected successfully.'
        }, status=status.HTTP_200_OK)


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
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        