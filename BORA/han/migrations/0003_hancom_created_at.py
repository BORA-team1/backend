# Generated by Django 4.2.4 on 2023-08-10 08:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("han", "0002_hancom_mention"),
    ]

    operations = [
        migrations.AddField(
            model_name="hancom",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
