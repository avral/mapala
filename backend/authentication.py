from django.contrib.auth import get_user_model


class EmailAsUsernameBackend:
    """ Login by username """
    user_model = get_user_model()

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = self.user_model.objects.get(email=username)
        except self.user_model.DoesNotExist:
            return None
        else:
            if user.is_active and user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        try:
            return self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            return None
