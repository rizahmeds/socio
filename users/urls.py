from django.urls import include, path
from rest_framework import routers

from users.views import LoginView, SignupView, UserViewSet, FriendshipViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friends', FriendshipViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]