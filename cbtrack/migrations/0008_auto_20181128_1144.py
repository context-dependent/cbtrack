# Generated by Django 2.1.3 on 2018-11-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbtrack', '0007_auto_20181128_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(choices=[('o', 'Non-trades'), ('a', 'Apprentice'), ('j', 'Journeyperson')], default='a', max_length=100),
        ),
        migrations.AlterField(
            model_name='payperiodconfig',
            name='pay_schedule',
            field=models.CharField(choices=[('twice_per_month', 'Twice per month'), ('monthly', 'Monthly'), ('every_two_weeks', 'Every two weeks')], default='every_two_weeks', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='org_type',
            field=models.CharField(blank=True, choices=[('sp', 'Service Provider'), ('emp', 'Employer')], max_length=100, null=True),
        ),
    ]
