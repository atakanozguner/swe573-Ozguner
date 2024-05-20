from django import forms
from .models import Community, Post, CommunityTemplate
import json


DATA_TYPE_CHOICES = [
    ("string", "String"),
    ("integer", "Integer"),
    ("boolean", "Boolean"),
    # Add more data types as needed
]


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["name", "description"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class TemplateForm(forms.Form):
    name = forms.CharField(max_length=100)
    fields = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )  # This will hold the JSON representation of the fields

    def clean_fields(self):
        data = self.cleaned_data["fields"]
        try:
            fields = json.loads(data)
        except (TypeError, ValueError):
            raise forms.ValidationError("Invalid fields data")
        return fields


class DynamicPostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields")
        super(DynamicPostForm, self).__init__(*args, **kwargs)
        for field in fields:
            field_type = field.get("type")
            field_name = field.get("name")
            if field_type == "str":
                self.fields[field_name] = forms.CharField(
                    label=field_name, max_length=255
                )
            elif field_type == "int":
                self.fields[field_name] = forms.IntegerField(label=field_name)
            elif field_type == "bool":
                self.fields[field_name] = forms.BooleanField(label=field_name)
            elif field_type == "datetime":
                self.fields[field_name] = forms.DateTimeField(label=field_name)
            elif field_type == "location":
                self.fields[field_name] = forms.CharField(
                    label=field_name, max_length=255
                )  # Custom handling needed


class DescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
