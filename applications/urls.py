from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_view, name='apply'),
    path('my/', views.my_applications_view, name='my_applications'),
    path('<int:application_id>/tracking/', views.application_tracking_view, name='tracking'),
    path('<int:application_id>/withdraw/', views.withdraw_application_view, name='withdraw'),
    path('recruiter/', views.recruiter_applicants_view, name='recruiter_applicants'),
    path('recruiter/<int:application_id>/', views.applicant_detail_view, name='applicant_detail'),
]
