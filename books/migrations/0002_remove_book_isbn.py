# Generated by Django 3.1.13 on 2021-08-06 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
    ]
