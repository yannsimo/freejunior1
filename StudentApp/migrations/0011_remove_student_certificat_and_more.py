# Generated by Django 5.0.6 on 2024-07-31 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0010_merge_20240731_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='certificat',
        ),
        migrations.RemoveField(
            model_name='student',
            name='portfolio_link',
        ),
        migrations.AddField(
            model_name='mission',
            name='nombre_de_candidature',
            field=models.IntegerField(default=0),
        ),
    ]
