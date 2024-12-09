# Generated by Django 5.1.2 on 2024-11-19 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db_examples", "0007_familyperson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="familyperson",
            name="father",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="father_of",
                to="db_examples.familyperson",
            ),
        ),
        migrations.AlterField(
            model_name="familyperson",
            name="mother",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mother_of",
                to="db_examples.familyperson",
            ),
        ),
    ]