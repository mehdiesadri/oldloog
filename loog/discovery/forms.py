from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models
from accounts.models import InvitedUser


class InitialTagsInputForm(forms.Form):
    user = forms.CharField(max_length=100)
    tag1 = forms.CharField(max_length=100)
    tag2 = forms.CharField(max_length=100)
    tag3 = forms.CharField(max_length=100)
    tag4 = forms.CharField(max_length=100)
    tag5 = forms.CharField(max_length=100)


class TagForm(forms.Form):
    tag_limit = 5

    comma_separated_tags = forms.CharField(
        max_length=1024,
        help_text=_("Separate tags by comma, or pressing the enter key."),
        widget=forms.TextInput(attrs={'data-role': 'tagsinput'})
    )

    def clean_comma_separated_tags(self):
        comma_separated_tags = self.cleaned_data.get("comma_separated_tags", "").split(",")

        if len(comma_separated_tags) < self.tag_limit:
            raise ValidationError(_(f'At least {self.tag_limit} tags required.'), code='invalid')

        initial_tags = ','.join([tag.strip() for tag in comma_separated_tags])
        return initial_tags


class InviteForm(forms.ModelForm, TagForm):
    email = forms.EmailField(
        help_text=_("Your invitation link will valid for next 24 hours.")
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_exists = models.User.objects.filter(email=email).exists()

        if user_exists:
            raise ValidationError(_("This email has an account!"), code='invalid')

        return email

    class Meta:
        model = InvitedUser
        fields = ["email", "comma_separated_tags"]


class InviteeTagForm(TagForm):
    user = forms.IntegerField(widget=forms.HiddenInput())

