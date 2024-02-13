from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'profile_image', 'password1', 'password1' )

class CustomAuthenticationForm(AuthenticationForm):
    pass