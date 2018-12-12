import datetime
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from functools import reduce

# Create your models here.
class Profile(models.Model):
    """
    A profile to go with each user. 

    Adds contact and organization details to employer and service 
    provider user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    org_type = models.CharField(max_length=100, choices={('emp', 'Employer'), ('sp', 'Service Provider')}, blank=True, null=True)
    org_name = models.CharField(max_length=100)
    org_description = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} at {self.org_name}'




class PayPeriodConfig(models.Model):
    """
    Pay period configuration

    I'm not sure this is the way we want to go. i think we could present
    an alternative that looks more like harvest, where we don't actually 
    need to create pay periods, just have a table for each week with 
    rows for each employee. 
    """
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    pay_schedule = models.CharField(
        max_length=100,
        choices={
            ('weekly', 'Every week'),
            ('every_two_weeks', 'Every two weeks'),
            ('twice_per_month', "Twice per month"),
            ('monthly', 'Monthly')
        },
        default='every_two_weeks'
    )
    start_from = models.DateField()


class Candidate(models.Model):
    """
    A Candidate is a person of interest for the evaluation of community benefits on the Finch LRT construction project
    They are a member of a historically disadvantaged or equity-seeking group of people who have either been hired
    to work on the project by a sub-contractor, or added to the verified list / job board by a service provider
    """
    # Minimum identifiers
    first_name = models.CharField(max_length=100, help_text='First name')
    last_name = models.CharField(max_length=100, help_text='Last name')
    email = models.EmailField(help_text='Email')
    phone = models.CharField(max_length=15, blank=True)
    
    TRADE_STATUS_CHOICES = {
        ('a', 'Apprentice'),
        ('j', 'Journeyperson'),
        ('o', 'Non-trades'),
    }

    trade_status = models.CharField(
        max_length=100, 
        default='a',
        choices=TRADE_STATUS_CHOICES,
        help_text='Trade status'
    )


    # Admin information
    date_added = models.DateTimeField('date registered in the tracker', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Community benefits information
    date_of_birth = models.DateField()
    racialized = models.BooleanField()
    indigenous = models.BooleanField()
    female = models.BooleanField()
    veteran = models.BooleanField()

    def get_absolute_url(self):
        return reverse('cbtrack:candidate-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ServiceDetail(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Deployment context
    job_board = models.BooleanField()
    verified_list = models.BooleanField()
    
    # Job board material
    """
    Job board material will be presented to employers without any identifying information about the candidate being 
    shared. The intention here is to have a place where employers can seek out community benefits eligible candidates, 
    flag their interest in contacting them to the relevant service provider, and have them arrange next steps
    """
    post_title = models.CharField(
        max_length=140, blank=True, null=True,
        default='A Snappy Post Title'
    )
    about_me = models.TextField(
        max_length=280, blank=True, null=True,
        default='I don\'t want to brag, but I\'m the best!'
    )
    how_help = models.TextField(
        max_length=280, blank=True, null=True,
        default='Here\'s what I\'m going to do for you'
    )
    top_trade = models.ManyToManyField(
        'TopTrade',
        blank=True
    )

    class Meta:
        permissions = (('service_detail_admin', 'Create, Update, and Delete service details'), )


    def __str__(self):
        return f'{self.candidate.first_name} {self.candidate.last_name}'


class TopTrade(models.Model):
    name = models.CharField(max_length=100)
    fa_icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EmploymentDetail(models.Model):
    """
    The employment detail table will allow candidates and employers to be linked, so that candidates can be linked
    to their payroll records, but it will allow us to preserve historical employment information if their job ends
    and they get a new one within the system
    """
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField(max_length=280)
    job_start_date = models.DateField()

    def get_hours_worked(self):
        hours_worked = PayrollRecord.objects \
            .filter(employee__pk=self.pk) \
            .aggregate(Sum('hours')) 
        return hours_worked

    def __str__(self):
        return f'{self.candidate} -- {self.job_title}' 

    class Meta:
        permissions = (('employment_detail_admin', 'Create, Update, and Delete employment details'), )


class PayPeriod(models.Model):
    """
    Pay periods define ranges of time for which employees are paid
    Each pay period has an associated employer user, a start date, an end date, and 0:n associated payroll records
    """
    # Admin information
    date_added = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    trade_hours = models.IntegerField(help_text='total trade hours worked', blank = True, null = True)
    created_by = models.ForeignKey(
        User, max_length=100, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    employment_detail = models.ManyToManyField(
        EmploymentDetail, 
        help_text='Select candidates that worked during this period'
    )
    


class PayrollRecord(models.Model):
    """
    Each individual payroll record contains the hours for one employee at one employer worked during one pay period
    Employers will only have to enter the hours here for now, but we may want to think about more information
    I'm thinking maybe a star rating system????
    """
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmploymentDetail, on_delete=models.CASCADE)
    hours = models.IntegerField(null=True, blank = True)
    stars = models.IntegerField(blank=True, null = True)


class ExpressionOfInterest(models.Model):
    """
    Employers will be able to create expressions of interest for candidates
    visible on the job board. When an employer creates an expression of interest
    the service provider handling the candidate's posting will be notified 
    through the application
    """
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    employment_detail = models.ForeignKey(
        EmploymentDetail, 
        on_delete=models.SET_NULL, 
        blank=True, null=True
    )
    employer_notes = models.TextField(
        max_length=500,
        blank=True, null=True
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Generate user profile object record any time a user is created 
    """
    if created:
        Profile.objects.create(user=instance)

