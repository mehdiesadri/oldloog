from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10, required=False)
    location = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "location",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.location = self.cleaned_data["location"]
        if commit:
            user.save()
        return user
