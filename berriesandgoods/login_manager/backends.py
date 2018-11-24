from home.models import Users


class UserBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            return Users.objects.raw(
                f"""SELECT * FROM users WHERE
                                     email='{username}' AND
                                     password='{password}';"""
            )[0]
        except IndexError:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.raw(
                f"""SELECT * FROM USERS WHERE
                                     idusers='{user_id}'"""
            )[0]
        except IndexError:
            return None
