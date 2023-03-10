from django import forms

from schemas.models import Schema


class CreateSchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')
