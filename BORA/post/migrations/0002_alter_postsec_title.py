# Generated by Django 4.2.4 on 2023-08-05 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postsec",
            name="title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]