# Generated by Django 4.2.4 on 2023-08-21 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pendinguser",
            old_name="created_at",
            new_name="otp_created_at",
        ),
        migrations.RemoveField(
            model_name="pendinguser",
            name="id",
        ),
        migrations.RemoveField(
            model_name="pendinguser",
            name="otp",
        ),
        migrations.RemoveField(
            model_name="pendinguser",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="pendinguser",
            name="user_ptr",
            field=models.OneToOneField(
                auto_created=True,
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
