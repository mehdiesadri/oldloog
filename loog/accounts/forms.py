from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from discovery.forms import TagForm
from .models import Profile, InvitedUser, User

User = get_user_model()


class RegisterForm(UserCreationForm, TagForm):
    def __init__(self, *args, **kwargs):
        sociallogin = kwargs.pop("sociallogin")
        print(sociallogin)
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['comma_separated_tags'].label = 'Inviter Tags'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email already exists."))
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "location", "birthdate", "preferences"]


class InviteForm(forms.ModelForm, TagForm):
    email = forms.EmailField(
        help_text=_("Your invitation link will valid for next 24 hours.")
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            raise ValidationError(_("This email has an account!"), code='invalid')

        return email

    class Meta:
        model = InvitedUser
        fields = ["email", "comma_separated_tags"]
