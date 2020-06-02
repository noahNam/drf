from rest_framework.throttling import UserRateThrottle


class UserMinThrottle(UserRateThrottle):
    scope = 'user_min'
