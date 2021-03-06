# Generated by Django 2.1.3 on 2018-12-05 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbtrack', '0025_auto_20181205_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(choices=[('a', 'Apprentice'), ('j', 'Journeyperson'), ('o', 'Non-trades')], default='a', help_text='Trade status', max_length=100),
        ),
        migrations.AlterField(
            model_name='payperiodconfig',
            name='pay_schedule',
            field=models.CharField(choices=[('monthly', 'Monthly'), ('twice_per_month', 'Twice per month'), ('every_two_weeks', 'Every two weeks')], default='every_two_weeks', max_length=100),
        ),
        migrations.AlterField(
            model_name='payrollrecord',
            name='hours',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='payrollrecord',
            name='stars',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='org_type',
            field=models.CharField(blank=True, choices=[('sp', 'Service Provider'), ('emp', 'Employer')], max_length=100, null=True),
        ),
    ]
