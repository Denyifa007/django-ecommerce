# Generated by Django 4.1.7 on 2023-05-29 06:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_ordered_data_orderplaced_ordered_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='ref',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
