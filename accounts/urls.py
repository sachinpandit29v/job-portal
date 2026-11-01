from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', lambda request: redirect('accounts:register_seeker'), name='register'),
    path('register/seeker/', views.register_seeker_view, name='register_seeker'),
    path('register/recruiter/', views.register_recruiter_view, name='register_recruiter'),
    path('profile/', views.profile_view, name='profile'),
    path('resume/', views.resume_upload_view, name='resume'),
    path('change-password/', views.change_password_view, name='change_password'),
]
