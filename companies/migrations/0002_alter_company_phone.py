# Generated by Django 5.1.7 on 2025-03-31 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
