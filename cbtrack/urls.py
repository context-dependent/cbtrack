from django.urls import path

from . import views

app_name = 'cbtrack'
urlpatterns = [
    path('', views.my_candidates, name='index'),
    path('verified-list/', views.verified_list_filter, name ='verified-list'),
    path('job-board/', views.job_board_filter, name = 'job-board'),

    # Candidate CRUD pages
    path(
    	'candidate/<int:pk>/', 
    	views.CandidateDetailView.as_view(), 
    	name='candidate-detail'
    ),
    path(
    	'add-candidate/', 
    	views.CandidateCreateView.as_view(), 
    	name='candidate_create'
    ),
    path(
    	'candidate/<int:pk>/edit/',
    	views.CandidateUpdateView.as_view(),
    	name='candidate_create'
    ), 

    # Service Detail CRUD pages
    path(
    	'candidate/<int:pk>/add-service-detail/',
    	views.ServiceDetailCreateView.as_view(),
    	name='service-detail_create'
    ),
    path(
    	'service-detail/<int:pk>/update/',
    	views.ServiceDetailUpdateView.as_view(),
    	name='service-detail_update'
    ),
    path(
    	'service-detail/<int:pk>/delete/',
    	views.ServiceDetailDeleteView.as_view(),
    	name='service-detail_delete'
    ),

    # Employment Detail CRUD pages
    path(
    	'candidate/<int:pk>/add-employment-detail/',
    	views.EmploymentDetailCreateView.as_view(),
    	name='employment-detail_create'
    ),
    path(
    	'employment-detail/<int:pk>/update/',
    	views.EmploymentDetailUpdateView.as_view(),
    	name='employment-detail_update'
    ),
    path(
    	'employment-detail/<int:pk>/delete/',
    	views.EmploymentDetailDeleteView.as_view(),
    	name='employment-detail_delete'
    ),
    path(
    	'hours-tracker/',
    	views.hours_tracker_home, 
    	name='hours-tracker'
    ),

    # Pay period Configuration crud pages
    path(
        'configure-pay-period/',
        views.PayPeriodConfigCreateView.as_view(), 
        name='configure-pay-period'
    ),
    path(
        'pay-period-config/<int:pk>/edit',
        views.PayPeriodConfigUpdateView.as_view(),
        name='pay-period-config_update'
    ),
    
    # Pay period CRUD pages
    path(
        'new-pay-period/',
        views.PayPeriodCreateView.as_view(),
        name='pay-period_create'
    ),
    # path(
    #     'pay-period/<int:pk>/edit',
    #     views.PayPeriodUpdateView.as_view(), 
    #     name='pay-period_update'
    # ),
    # path(
    #     'pay-period/<int:pk>/delete',
    #     views.PayPeriodDeleteView.as_view(),
    #     name='pay-period_delete'
    # ),

    # Payroll record CRUD pages
    path(
        'pay-period/<int:pay_period_id>/manage-records', 
        views.manage_payroll_records, 
        name='manage-records'
    ),
    path(
        'candidate/<int:pk>/offer_job', 
        views.ExpressionOfInterestCreateView.as_view(), 
        name='eoi_create'
    ),

    # Profile detail view
    path(
        'profile/<int:pk>/',
        views.ProfileDetailView.as_view(),
        name='profile-detail'
    )
    


]
