# Generated by Django 3.1.13 on 2021-08-06 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_bookedition_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrowed', models.DateTimeField()),
                ('date_returned', models.DateTimeField(auto_now_add=True)),
                ('return_status', models.CharField(choices=[('ON-TIME', 'ON-TIME'), ('LATE', 'LATE')], max_length=100)),
                ('damage_status', models.BooleanField(default=False)),
                ('damage_description', models.CharField(blank=True, max_length=200, null=True)),
                ('fine', models.PositiveIntegerField()),
                ('book_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.bookedition')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrowed', models.DateTimeField(auto_now_add=True)),
                ('date_to_return', models.DateTimeField()),
                ('book_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.bookedition')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.customer')),
            ],
        ),
    ]
