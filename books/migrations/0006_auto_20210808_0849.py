# Generated by Django 3.1.13 on 2021-08-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedition',
            name='ISBN',
            field=models.CharField(max_length=10),
        ),
    ]