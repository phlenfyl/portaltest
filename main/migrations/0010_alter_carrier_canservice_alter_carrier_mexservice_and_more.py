# Generated by Django 5.0.2 on 2024-05-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_carrier_liftgates_carrier_scac_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='canservice',
            field=models.TextField(blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']", null=True, verbose_name='Canada Service'),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='mexservice',
            field=models.TextField(blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']", null=True, verbose_name='Mexico Service'),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='usservice',
            field=models.TextField(blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']", null=True, verbose_name='Domestic Service'),
        ),
    ]
