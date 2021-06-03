from django import forms


class InitialTagsInputForm(forms.Form):
    user = forms.CharField(max_length=100)
    tag1 = forms.CharField(max_length=100)
    tag2 = forms.CharField(max_length=100)
    tag3 = forms.CharField(max_length=100)
    tag4 = forms.CharField(max_length=100)
    tag5 = forms.CharField(max_length=100)
