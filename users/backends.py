from .models import MyUser


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None