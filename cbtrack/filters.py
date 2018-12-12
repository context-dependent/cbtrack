import django_filters as df 
from django import forms
from .models import ServiceDetail, TopTrade

class ServiceDetailFilter(df.FilterSet):
	candidate__first_name = df.CharFilter(lookup_expr='icontains')
	candidate__last_name = df.CharFilter(lookup_expr='icontains')
	candidate__email = df.CharFilter(lookup_expr='icontains')
	service_provider = df.CharFilter(lookup_expr='icontains')

	class Meta: 
		model = ServiceDetail
		fields = [
			'candidate__first_name',
			'candidate__last_name',
			'candidate__email',
			'service_provider'
		]

class JobBoardFilter(df.FilterSet):
	top_trade = df.ModelMultipleChoiceFilter(
		queryset=TopTrade.objects.all(),
		widget = forms.CheckboxSelectMultiple
	)
	service_provider__profile__org_name = df.CharFilter(lookup_expr='icontains')
	class Meta:
		model = ServiceDetail
		fields = [
			'top_trade',
			'candidate__date_added',
			'service_provider__profile__org_name'
		]