# Generated by Django 2.1.3 on 2018-11-17 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('post_title', models.CharField(max_length=140)),
                ('about_me', models.TextField(max_length=280)),
                ('how i can help', models.TextField(max_length=280)),
                ('job_board', models.BooleanField()),
                ('verified_list', models.BooleanField()),
                ('employed', models.BooleanField()),
                ('date_added', models.DateTimeField(verbose_name='date registered in the tracker')),
                ('added_by', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('racialized', models.BooleanField()),
                ('indigenous', models.BooleanField()),
                ('female', models.BooleanField()),
                ('veteran', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('user_id', models.CharField(max_length=280)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('job_description', models.CharField(max_length=280)),
                ('job_start_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.Candidate')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total trade hours worked', models.IntegerField()),
                ('added_by', models.CharField(max_length=100)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='PayPeriodConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_schedule', models.CharField(choices=[('twice_per_month', 'Twice per month'), ('monthly', 'Monthly'), ('every_two_weeks', 'Every two weeks')], default='every_two_weeks', max_length=100)),
                ('start_from', models.DateField()),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='PayrollRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('stars', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.EmploymentDetail')),
                ('pay_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbtrack.PayPeriod')),
            ],
        ),
    ]
