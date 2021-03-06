# Generated by Django 2.1.3 on 2018-12-04 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbtrack', '0019_auto_20181130_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(choices=[('o', 'Non-trades'), ('j', 'Journeyperson'), ('a', 'Apprentice')], default='a', help_text='Trade status', max_length=100),
        ),
        migrations.AlterField(
            model_name='employmentdetail',
            name='job_description',
            field=models.TextField(max_length=280),
        ),
        migrations.AlterField(
            model_name='payperiodconfig',
            name='employer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payperiodconfig',
            name='pay_schedule',
            field=models.CharField(choices=[('monthly', 'Monthly'), ('every_two_weeks', 'Every two weeks'), ('twice_per_month', 'Twice per month')], default='every_two_weeks', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='org_type',
            field=models.CharField(blank=True, choices=[('emp', 'Employer'), ('sp', 'Service Provider')], max_length=100, null=True),
        ),
    ]
