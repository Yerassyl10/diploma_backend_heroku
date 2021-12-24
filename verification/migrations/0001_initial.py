# Generated by Django 4.0 on 2021-12-22 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='emailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('isVerified', models.BooleanField(default=False)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
    ]