from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    pass

    class Meta():
        model = User
        fields= ['username', 'password1', 'email', 'password2']