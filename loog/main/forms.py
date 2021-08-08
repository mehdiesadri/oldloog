from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].help_text = _("Enter the email that you received the invitation link.")

    def clean_email(self):
        email = super(RegisterForm, self).clean_email()

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

