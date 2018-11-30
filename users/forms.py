from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("username", "email")

class UserForm(AuthenticationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("username", "password")