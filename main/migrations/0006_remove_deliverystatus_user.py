# Generated by Django 5.0.2 on 2024-05-09 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_deliverystatus_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverystatus',
            name='user',
        ),
    ]
