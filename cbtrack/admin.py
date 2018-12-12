from django.contrib import admin
from .models import Candidate, TopTrade, Profile, ServiceDetail, EmploymentDetail, PayPeriod, PayrollRecord, PayPeriodConfig

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Profile)
admin.site.register(ServiceDetail)
admin.site.register(EmploymentDetail)
admin.site.register(PayPeriod)
admin.site.register(PayrollRecord)
admin.site.register(TopTrade)
admin.site.register(PayPeriodConfig)