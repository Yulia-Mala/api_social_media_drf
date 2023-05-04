# Generated by Django 4.2 on 2023-04-23 22:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sm_app", "0004_alter_post_image"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(
                fields=("post", "user"), name="1 like from 1 user to 1 post"
            ),
        ),
    ]