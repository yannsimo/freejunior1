# Generated by Django 5.0.6 on 2024-08-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="external_sso_id",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="user",
            name="is_sso_user",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="last_sso_login",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
