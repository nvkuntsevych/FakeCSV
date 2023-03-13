from django import forms

from schemas.models import Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')


ColumnFormSet = forms.modelformset_factory(
    Column, 
    fields = ('name', 'type', 'order'),
    extra=1,
)
