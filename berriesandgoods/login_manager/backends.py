from django.conf import settings
from django.contrib.auth.hashers import check_password

from home.models import Users


class UserBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            print("Trying to get user!")
            user = Users.objects.get(email=username)
        except Users.DoesNotExist:
            print("Failed to get user!")
            return None
        if user.email == username and check_password(
            password, user.password
        ):
            return user
        print("Incorrect Password!")
        return None

    def get_user(self, user_id):
        try:
            Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.username == settings.ADMIN_LOGIN:
            return user_obj.has_perm(perm, obj)
        return False
