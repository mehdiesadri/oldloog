from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

from .models import Profile


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.HiddenInput(attrs={'readonly': True})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "location", "birthdate", "preferences"]
