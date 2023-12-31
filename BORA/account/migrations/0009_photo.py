# Generated by Django 4.2.4 on 2023-08-15 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_remove_user_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="PHOTO",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="blog_photo"),
                ),
            ],
        ),
    ]
