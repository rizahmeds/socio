from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled
from rest_framework.response import Response

class CustomThrottledResponse(Throttled):
    
    def get_retry_after(self):
        return self.wait

    def get_full_details(self):
        return {
            'detail': 'You have exceeded the rate limit. You can make up to 3 friend requests per minute.',
            'retry_after': self.get_retry_after()
        }

    def __call__(self, request, context):
        self.wait = self.duration - (self.now - self.last_request)
        return Response(self.get_full_details(), status=self.status_code)



class FriendRequestRateThrottle(UserRateThrottle):
    """
    Limit the rate of friend requests to 3 per minute.
    """
    rate = '3/minute'
    throttled_response = CustomThrottledResponse

    def wait(self):
        return self.duration

    def get_scope(self):
        return 'friend-requests'