# Generated by Django 5.0.6 on 2024-07-20 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0006_alter_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
