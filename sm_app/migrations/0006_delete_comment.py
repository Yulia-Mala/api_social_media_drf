# Generated by Django 4.2 on 2023-04-23 23:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sm_app", "0005_like_1_like_from_1_user_to_1_post"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
    ]
