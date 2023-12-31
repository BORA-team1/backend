# Generated by Django 3.0.8 on 2023-08-16 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_photo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PHOTO',
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile'),
        ),
    ]
