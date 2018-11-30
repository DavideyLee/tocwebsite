from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("username", "email")