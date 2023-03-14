from django.contrib.auth import get_user_model
from django.db import models


COLUMN_SEPARATOR_CHOICES = (
    (",", "Comma (,)"),
    (";", "Semicolon (;)"),
)
STRING_CHARACTER_CHOICES = (
    ('"', 'Double-quote (")'),
    ("'", "Single-quote (')"),
)
COLUMN_TYPE_CHOICES = (
    ("1", "Full name"),
    ("2", "Email"),
    ("3", "Phone number"),
    ("4", "Address"),
    ("5", "Date"),
)


class Schema(models.Model):
    name = models.CharField(max_length=50)
    column_separator = models.CharField(max_length=1, default=",",
                                        choices=COLUMN_SEPARATOR_CHOICES)
    string_character = models.CharField(max_length=1, default='"',
                                        choices=STRING_CHARACTER_CHOICES)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='schemas')

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=COLUMN_TYPE_CHOICES)
    order = models.IntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,
                               related_name='columns')

    def __str__(self):
        return self.name


class DataSet(models.Model):
    path = models.FilePathField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,
                               related_name='datasets')

    @classmethod
    def get_next_sequence_number(cls, schema_id):
        return cls.objects.filter(schema_id=schema_id).count()
