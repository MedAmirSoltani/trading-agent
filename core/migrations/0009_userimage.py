# Generated by Django 4.2.9 on 2024-04-12 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_remove_customuser_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserImage",
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
                ("image", models.ImageField(upload_to="user_images/")),
            ],
        ),
    ]
