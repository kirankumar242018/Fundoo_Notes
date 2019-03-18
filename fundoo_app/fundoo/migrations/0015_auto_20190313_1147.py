# Generated by Django 2.1.7 on 2019-03-13 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fundoo', '0014_auto_20190313_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='collaborate',
            field=models.ManyToManyField(blank=True, null=True, related_name='collaborated_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]