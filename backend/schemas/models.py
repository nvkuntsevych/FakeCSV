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


class Schema(models.Model):
    name = models.CharField(max_length=50)
    column_separator = models.CharField(max_length=1, choices=COLUMN_SEPARATOR_CHOICES, default=",")
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER_CHOICES, default='"')
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='schemas')

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    order = models.IntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='columns')

    def __str__(self):
        return self.name
