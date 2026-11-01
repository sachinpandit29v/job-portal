from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('seeker/', views.seeker_dashboard_view, name='seeker'),
    path('recruiter/', views.recruiter_dashboard_view, name='recruiter'),
    path('recruiter/analytics/', views.recruiter_analytics_view, name='recruiter_analytics'),
    path('admin-panel/', views.admin_dashboard_view, name='admin'),
    path('admin-panel/user/<int:user_id>/toggle/', views.admin_toggle_user_view, name='admin_toggle_user'),
    path('admin-panel/category/<int:category_id>/<str:action>/', views.admin_category_action_view, name='admin_category_action'),
    path('admin-panel/category/add/', views.admin_category_add_view, name='admin_category_add'),
    path('admin-panel/report/<int:report_id>/<str:action>/', views.admin_report_action_view, name='admin_report_action'),
]
