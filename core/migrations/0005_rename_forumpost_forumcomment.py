# Generated by Django 4.2.9 on 2024-03-25 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_forumtopic_alter_forumpost_topic"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ForumPost",
            new_name="ForumComment",
        ),
    ]
