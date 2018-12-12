# Generated by Django 2.1.3 on 2018-12-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbtrack', '0023_auto_20181205_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='trade_status',
            field=models.CharField(choices=[('j', 'Journeyperson'), ('a', 'Apprentice'), ('o', 'Non-trades')], default='a', help_text='Trade status', max_length=100),
        ),
    ]
