from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.HiddenInput(attrs={'readonly': True})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

