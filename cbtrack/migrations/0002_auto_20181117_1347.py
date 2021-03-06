# Generated by Django 2.1.3 on 2018-11-17 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbtrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(default='Apprentice', max_length=100),
        ),
        migrations.AlterField(
            model_name='payperiodconf',
            name='pay_schedule',
            field=models.CharField(choices=[('every_two_weeks', 'Every two weeks'), ('monthly', 'Monthly'), ('twice_per_month', 'Twice per month')], default='every_two_weeks', max_length=100),
        ),
    ]
