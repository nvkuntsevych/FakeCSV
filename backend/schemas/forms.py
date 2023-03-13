from django import forms

from schemas.models import Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')


ColumnCreateFormSet = forms.modelformset_factory(
    Column,
    fields=('name', 'type', 'order'),
    extra=1
)

ColumnUpdateFormSet = forms.modelformset_factory(
    Column,
    fields=('name', 'type', 'order'),
    extra=0
)
