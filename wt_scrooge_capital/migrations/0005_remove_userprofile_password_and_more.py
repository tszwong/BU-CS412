# Generated by Django 5.1.2 on 2024-11-15 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wt_scrooge_capital", "0004_userprofile_password_userprofile_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="password",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="username",
        ),
    ]
