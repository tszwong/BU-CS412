# Generated by Django 5.1.2 on 2024-11-19 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db_examples", "0002_bankaccount_balance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Student",
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
                ("name", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=120)),
                ("number", models.CharField(max_length=10)),
                ("students", models.ManyToManyField(to="db_examples.student")),
            ],
        ),
    ]
