# Generated by Django 5.1.4 on 2025-02-21 12:30

import src.core.entity
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
                ("user_id", models.CharField(max_length=255)),
                (
                    "role",
                    models.CharField(
                        choices=[("U", "User"), ("D", "Dietetic")],
                        default="U",
                        max_length=3,
                    ),
                ),
                ("website", models.URLField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, src.core.entity.Entity),
        ),
    ]
