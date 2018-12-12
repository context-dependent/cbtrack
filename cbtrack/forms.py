from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML
from .models import Candidate, ServiceDetail, EmploymentDetail, PayPeriod, PayPeriodConfig, PayrollRecord


class AddCandidateFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AddCandidateFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            HTML('<div class="d-flex"><hr class="my-auto flex-grow-1"><div class="px-4">CANDIDATE DETAILS</div><hr class="my-auto flex-grow-1"></div>'),
            Div(
                Div('first_name', css_class='col-md-4'),
                Div('last_name', css_class='col-md-4'),
                Div('date_of_birth', css_class='col-md-4', css_type = 'date'),
                Div('email', css_class='col-md-6'),
                Div('phone', css_class='col-md-6'),
                Div('trade_status', css_class='col-md-4'),
                css_class='row',
            ),
            HTML('<div class="d-flex"><hr class="my-auto flex-grow-1"><div class="px-4">COMMUNITY BENEFITS INFORMATION</div><hr class="my-auto flex-grow-1"></div>'),
            Div(
                Div('indigenous', css_class='col-md-2'),
                Div('racialized', css_class='col-md-2'),
                Div('female', css_class='col-md-2'),
                Div('veteran', css_class='col-md-2'),
                css_class='row',
                title='Community Benefits Criteria'
            ),
        )
        self.form_tag = False


class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
            'trade_status',
            'date_of_birth',
            'indigenous',
            'racialized',
            'female',
            'veteran'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs = {'type': 'date'}),
            'email': forms.EmailInput()
        }


class AddServiceDetailFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AddServiceDetailFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.add_input(Submit('submit', 'Submit'))


class AddServiceDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddServiceDetailForm, self).__init__(*args, **kwargs)
        self.helper = AddServiceDetailFormHelper()

    class Meta:
        model = ServiceDetail
        exclude = ['candidate', 'service_provider']



class AddEmploymentDetailFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AddEmploymentDetailFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.add_input(Submit('submit', 'Submit'))



class AddEmploymentDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddEmploymentDetailForm, self).__init__(*args, **kwargs)
        self.helper = AddEmploymentDetailFormHelper()

    class Meta:
        model = EmploymentDetail
        exclude = ['candidate', 'employer']


class AddPayPeriodForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		u = kwargs.pop('user')
		super(AddPayPeriodForm, self).__init__(*args, **kwargs)
		self.fields['employment_detail'].queryset = EmploymentDetail.objects.filter(employer=u)

	class Meta: 
		model = PayPeriod
		fields = ['start_date', 'end_date', 'trade_hours', 'employment_detail']


class ManageRecordsFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(ManageRecordsFormHelper, self).__init__(*args, **kwargs)
		self.form_method = "post"
		self.layout = (
			Div(
				Div('employee', css_class='col-md-4'),
				Div('title', css_class='col-md-4'),
                Div('subtitle', css_class='col-md-4'),
                css_class='row'
			)

		)
		self.add_input(Submit('submit', 'Submit'))
		self.template = 'bootstrap/table_inline_formset.html'
