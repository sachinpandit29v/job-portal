from django.urls import path
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('company/', views.company_profile_view, name='company_profile'),
]
