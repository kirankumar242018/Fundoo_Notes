# Generated by Django 2.1.7 on 2019-03-06 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundoo', '0005_remove_profile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
