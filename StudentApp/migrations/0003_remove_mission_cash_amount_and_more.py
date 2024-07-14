# Generated by Django 5.0.6 on 2024-07-14 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0002_alter_mission_cash_amount_alter_mission_equity_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='cash_amount',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='equity_offer',
        ),
        migrations.AlterField(
            model_name='student',
            name='study_level',
            field=models.CharField(choices=[('Bac+3', 'Bac+3'), ('Bac+4', 'Bac+4'), ('Bac+5', 'Bac+5')], max_length=5, null=True),
        ),
    ]