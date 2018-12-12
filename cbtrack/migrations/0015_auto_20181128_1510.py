# Generated by Django 2.1.3 on 2018-11-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('cbtrack', '0014_auto_20181128_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(choices=[('j', 'Journeyperson'), ('a', 'Apprentice'), ('o', 'Non-trades')], default='a', help_text='Trade status', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='org_type',
            field=models.CharField(blank=True, choices=[('emp', 'Employer'), ('sp', 'Service Provider')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='servicedetail',
            name='top_trade',
            field=models.ManyToManyField(blank=True, to='cbtrack.TopTrade'),
        ),
    ]