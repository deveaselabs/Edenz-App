# Generated by Django 5.0.4 on 2024-04-12 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_employee_cnic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='cnic',
        ),
    ]
