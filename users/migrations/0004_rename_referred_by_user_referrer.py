# Generated by Django 4.2.4 on 2023-08-21 12:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_delete_pendinguser"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="referred_by",
            new_name="referrer",
        ),
    ]
