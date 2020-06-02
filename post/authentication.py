from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

User = get_user_model()


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.GET.get("username")
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Not found user')

        return (user, None)
