from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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



