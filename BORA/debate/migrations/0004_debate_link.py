# Generated by Django 3.0.8 on 2023-08-16 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0003_auto_20230817_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate',
            name='link',
            field=models.TextField(null=True),
        ),
    ]
