# Generated by Django 4.2.5 on 2023-12-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("virtualdict", "0010_reviews"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviews",
            name="review",
            field=models.BooleanField(null=True),
        ),
    ]
