# Generated by Django 3.1.13 on 2021-08-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_borrowreceipt_returnreceipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_cover',
            field=models.ImageField(blank=True, default='image-not-found.png', null=True, upload_to=''),
        ),
    ]