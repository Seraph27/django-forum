# Generated by Django 3.0.5 on 2020-07-03 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rex_app', '0008_directmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directmessage',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_user_reverse', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='directmessage',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_user_reverse', to=settings.AUTH_USER_MODEL),
        ),
    ]
