# Generated by Django 2.2.11 on 2021-11-19 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='Date_of_Birth',
            new_name='birthday',
        ),
    ]
