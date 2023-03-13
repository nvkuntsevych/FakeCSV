# Generated by Django 4.1.7 on 2023-03-13 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('column_separator', models.CharField(choices=[(',', 'Comma (,)'), (';', 'Semicolon (;)')], default=',', max_length=1)),
                ('string_character', models.CharField(choices=[('"', 'Double-quote (")'), ("'", "Single-quote (')")], default='"', max_length=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('1', 'Full name'), ('2', 'Email'), ('3', 'Phone number')], max_length=1)),
                ('order', models.IntegerField()),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='schemas.schema')),
            ],
        ),
    ]
