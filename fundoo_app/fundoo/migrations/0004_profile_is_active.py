# Generated by Django 2.1.7 on 2019-03-06 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundoo', '0003_auto_20190305_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
