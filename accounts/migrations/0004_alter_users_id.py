# Generated by Django 4.0 on 2021-12-22 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211119_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]