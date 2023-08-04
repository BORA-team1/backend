# Generated by Django 4.2.4 on 2023-08-03 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_user_follow"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="follow",
            field=models.ManyToManyField(
                related_name="follower", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("남", "남"), ("여", "여")], default="여", max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_publisher",
            field=models.BooleanField(default=False),
        ),
    ]