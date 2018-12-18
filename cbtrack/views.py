from django.http import HttpResponseRedirect
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Candidate, ServiceDetail, ExpressionOfInterest, EmploymentDetail, PayPeriodConfig, PayPeriod, PayrollRecord, Profile
from .filters import ServiceDetailFilter, JobBoardFilter
from django.contrib.auth.models import User
from .forms import AddCandidateFormHelper, AddPayPeriodForm, AddCandidateForm, AddServiceDetailForm, AddEmploymentDetailForm, AddEmploymentDetailFormHelper, ManageRecordsFormHelper



def index(request):
    candidates = Candidate.objects.all()
    return render(request, template_name='cbtrack/index.html', context={'candidates': candidates})


class CandidateDetailView(generic.DetailView):
    model = Candidate


class CandidateCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = AddCandidateForm
    model = Candidate

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)
        form.helper = AddCandidateFormHelper()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        u = self.request.user
        if u.has_perm('cbtrack.service_detail_admin'):
            return reverse('cbtrack:service-detail_create', args=(self.object.id, ))
        elif u.has_perm('cbtrack.employment_detail_admin'):
            return reverse('cbtrack:employment-detail_create', args=(self.object.id, ))
        else: 
            return reverse('index')



class CandidateUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = AddCandidateForm
    model = Candidate

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)
        form.helper = AddCandidateFormHelper()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        u = self.request.user
        if u.has_perm('service_detail_admin'):
            return reverse('cbtrack:service-detail_create', args=(self.object.id, ))
        elif u.has_perm('employment_detail_admin'):
            return reverse('cbtrack:employment-detail_create', args=(self.object.id, ))
        else: 
            return reverse('index')



class ServiceDetailCreateView(LoginRequiredMixin, generic.CreateView):
    model = ServiceDetail
    form_class = AddServiceDetailForm

    def form_valid(self, form):
        form.instance.candidate = get_object_or_404(
            Candidate, 
            pk=self.kwargs['pk']
        )
        form.instance.service_provider = self.request.user
        return super(ServiceDetailCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cbtrack:candidate-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        ctx = super(ServiceDetailCreateView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.kwargs['pk'])
        return ctx


class ServiceDetailUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ServiceDetail
    form_class = AddServiceDetailForm

    def get_success_url(self):
        return reverse(
                'cbtrack:candidate-detail', 
                kwargs={'pk': self.object.candidate.pk}
            )

    def get_context_data(self, **kwargs):
        ctx = super(ServiceDetailUpdateView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.object.candidate.pk)
        return ctx



class ServiceDetailDeleteView(generic.DeleteView):
    model = ServiceDetail

    def get_context_data(self, **kwargs):
        ctx = super(ServiceDetailDeleteView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.object.candidate.pk)
        return ctx

    def get_success_url(self):
        return reverse('cbtrack:candidate-detail', kwargs={'pk': self.object.candidate.pk})


class EmploymentDetailCreateView(LoginRequiredMixin, generic.CreateView):
    model = EmploymentDetail
    form_class = AddEmploymentDetailForm

    def form_valid(self, form):
        candidate = get_object_or_404(Candidate, pk=self.kwargs['pk'])
        service_details = ServiceDetail.objects.filter(candidate=candidate)
        service_details.update(job_board=False, verified_list=False)
        form.instance.candidate = candidate
        form.instance.employer = self.request.user
        return super(EmploymentDetailCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cbtrack:candidate-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        ctx = super(EmploymentDetailCreateView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.kwargs['pk'])
        return ctx


class EmploymentDetailUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmploymentDetail
    form_class = AddEmploymentDetailForm

    def get_success_url(self):
        return reverse('cbtrack:candidate-detail', kwargs={'pk': self.object.candidate.pk})

    def get_context_data(self, **kwargs):
        ctx = super(EmploymentDetailUpdateView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.object.candidate.pk)
        return ctx



class EmploymentDetailDeleteView(generic.DeleteView):
    model = EmploymentDetail

    def get_context_data(self, **kwargs):
        ctx = super(EmploymentDetailDeleteView, self).get_context_data(**kwargs)
        ctx["candidate"] = get_object_or_404(Candidate, pk=self.object.candidate.pk)
        return ctx

    def get_success_url(self):
        return reverse('cbtrack:candidate-detail', kwargs={'pk': self.object.candidate.pk})


@login_required
def my_candidates(request):
    user_id = request.user.pk
    u = get_object_or_404(User, pk=user_id)

    if u.has_perm('cbtrack.service_detail_admin'):
        d = ServiceDetail.objects.filter(service_provider__pk=user_id)
    elif u.has_perm('cbtrack.employment_detail_admin'):
        d = EmploymentDetail.objects.filter(employer__pk=user_id)
    else:
        d = {}

    return render(request, 'cbtrack/index_my_candidates.html', {'my_candidates': d})



@login_required
def add_candidate(self):
    ServiceDetailFormSet = modelformset_factory(
        Candidate, ServiceDetail, 
        fields=(
            'post_title', 
            'about_me',
            'how_help', 
            'job_board', 
            'verified_list',
        )
    )



class VerifiedListView(generic.ListView):
    model = ServiceDetail
    template_name = 'cbtrack/verified_list.html'
    context_object_name = 'verified_candidates'

    def get_queryset(self):
        return ServiceDetail.objects.filter(verified_list=True)


def verified_list_filter(request):
    candidate_list = ServiceDetail.objects.filter(verified_list=True)
    candidate_filter = ServiceDetailFilter(
        request.GET, 
        queryset=candidate_list
    )
    return render(
            request, 
            'cbtrack/verified_list_filter.html', 
            {'filter': candidate_filter}
        )
        

class JobBoardListView(generic.ListView):
    """
    View layer for list of job board postings. Filters ServiceDetail objects
    for candidates with job_board == True
    """
    model = ServiceDetail
    template_name = 'cbtrack/job_board.html'
    context_object_name = 'job_board_posts'

    def get_queryset(self):
        return ServiceDetail.objects.filter(job_board=True)


def job_board_filter(request):
    candidate_list = ServiceDetail.objects\
        .filter(job_board=True)\
        .order_by('-candidate__date_added')
    candidate_filter = JobBoardFilter(request.GET, queryset=candidate_list)
    return render(request, 'cbtrack/job_board_filter.html', {'filter': candidate_filter})


class MyCandidatesListView(generic.ListView):
    """
    View Layer that filters candidate objects for candidates created by
    the current user. 
    """
    model = Candidate
    context_object_name = 'my_candidates'
    template_name = 'cbtrack/my_candidates.html'

    def get_queryset(self):
        user_id = self.request.user
        return Candidate.objects.filter(created_by=user_id)


def hours_tracker_home(request):
    u_pk = request.user.pk
    u = get_object_or_404(User, pk=u_pk)
    try:  
        pay_period_config = PayPeriodConfig.objects.get(employer__pk=u_pk)
    except: 
        pay_period_config = 0

    pay_period_list = PayPeriod.objects.filter(created_by_id=u_pk)

    return render(
        request, 
        template_name = "cbtrack/hours_tracker_home.html",
        context = {
            'pay_period_config': pay_period_config,
            'pay_period_list': pay_period_list
        }
        )


class PayPeriodConfigCreateView(generic.CreateView):
    model = PayPeriodConfig
    fields = ['pay_schedule', 'start_from']

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super(PayPeriodConfigCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cbtrack:hours-tracker')


class PayPeriodConfigUpdateView(generic.UpdateView):
    model = PayPeriodConfig

    def get_success_url(self):
        return reverse('cbtrack:hours-tracker')


class PayPeriodCreateView(generic.CreateView):
    model = PayPeriod
    form_class = AddPayPeriodForm

    def get_form_kwargs(self):
        kwargs = super(PayPeriodCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        new_pp = form.save()
        jobs = form.cleaned_data['employment_detail']
        for job in jobs: 
            new_pr = PayrollRecord(
                employee=job, 
                pay_period=PayPeriod.objects.get(pk = new_pp.pk)
            )
            new_pr.save()

        return super(PayPeriodCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cbtrack:hours-tracker')



def manage_payroll_records(request, pay_period_id):

    pay_period = PayPeriod.objects.get(pk=pay_period_id)

    PayrollRecordInlineFormset = inlineformset_factory(
        PayPeriod, 
        PayrollRecord,  
        extra=0,
        fields=('employee', 'hours', 'stars', )
    )

    helper = ManageRecordsFormHelper


    if request.method == "POST":
        formset = PayrollRecordInlineFormset(request.POST, request.FILES, instance = pay_period)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/cbtrack/hours-tracker/')

    else: 
        formset = PayrollRecordInlineFormset(instance = pay_period)

    return render(request, 'cbtrack/manage_records.html', {'pay_period': pay_period, 'formset': formset, 'helper': helper})


class ExpressionOfInterestCreateView(generic.CreateView):
    model = ExpressionOfInterest
    fields = "__all__"

    def get_success_url(self): 
        return reverse('index')

    def form_valid(self, form, **kwargs):
        form.instance.employer = self.request.user
        return super(ExpressionOfInterestCreateView, self).form_valid(form)


class ExpressionOfInterestListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    
    class Meta: 
        model = ExpressionOfInterest

    def get_queryset(self, *args, **kwargs):
        u = self.request.user
        if u.has_perm('service_detail_admin'):
            return ExpressionOfInterest.objects.filter(candidate__created_by=u)
        elif u.has_perm('employment_detail_admin'):
            return ExpressionOfInterest.objects.filter(employer=u)
        else: 
            return reverse('index')



class ProfileDetailView(generic.DetailView):

    model = Profile


class ProfileListView(generic.ListView):

    class Meta: 
        model = Profile