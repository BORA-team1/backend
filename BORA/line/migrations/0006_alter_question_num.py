# Generated by Django 4.2.4 on 2023-08-07 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("line", "0005_rename_vote_postsec_question_que_postsec"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="num",
            field=models.IntegerField(null=True),
        ),
    ]
