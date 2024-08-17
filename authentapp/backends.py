
from django.contrib.auth.backends import BaseBackend
from .models import Usuario, Constructora

class UsuarioConstructoraBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            try:
                user = Constructora.objects.get(username=username)
            except Constructora.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            try:
                return Constructora.objects.get(pk=user_id)
            except Constructora.DoesNotExist:
                return None