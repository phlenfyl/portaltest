# Generated by Django 5.0.2 on 2024-05-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_order_note_alter_generatedreport_deliverystatus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
