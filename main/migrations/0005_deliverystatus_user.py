# Generated by Django 5.0.2 on 2024-05-09 16:40

import django.db.models.deletion
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_deliverystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverystatus',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]