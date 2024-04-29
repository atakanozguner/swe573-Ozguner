from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name']


class TemplateFieldForm(forms.Form):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('integer', 'Integer'),
    ]

    name = forms.CharField(max_length=200)
    type = forms.ChoiceField(choices=FIELD_TYPES)
    required = forms.BooleanField(required=False)