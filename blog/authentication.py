from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.core.validators import validate_email

class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        try:
            validate_email(username)
            user = CustomUser.objects.get(email=username)
        except:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return None
        if user.verified and user.password==password:
            
            return user
        
        return None
            
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None