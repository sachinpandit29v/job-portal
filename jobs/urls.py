from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('post/', views.post_job_view, name='post_job'),
    path('manage/', views.manage_jobs_view, name='manage_jobs'),
    path('saved/', views.saved_jobs_view, name='saved_jobs'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('<int:job_id>/edit/', views.edit_job_view, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job_view, name='delete_job'),
    path('<int:job_id>/toggle-save/', views.toggle_save_job_view, name='toggle_save'),
    path('<int:job_id>/report/', views.report_job_view, name='report_job'),
]
