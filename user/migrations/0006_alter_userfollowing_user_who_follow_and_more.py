# Generated by Django 4.2 on 2023-04-23 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_alter_userfollowing_user_who_follow_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfollowing",
            name="user_who_follow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="users_who_follow",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="userfollowing",
            name="user_who_influence",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="users_who_influence",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
