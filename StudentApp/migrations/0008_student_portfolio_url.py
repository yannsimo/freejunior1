# Generated by Django 5.0.6 on 2024-07-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0007_mission_disponible'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='portfolio_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
