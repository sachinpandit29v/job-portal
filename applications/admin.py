from django.contrib import admin
from .models import JobApplication, ApplicationStatusHistory, Interview

class StatusHistoryInline(admin.TabularInline):
    model = ApplicationStatusHistory
    extra = 0
    readonly_fields = ('previous_status', 'new_status', 'changed_by', 'remarks', 'created_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('seeker', 'job', 'current_status', 'created_at', 'updated_at')
    list_filter = ('current_status', 'job__company')
    search_fields = ('seeker__full_name', 'seeker__email', 'job__title')
    inlines = [StatusHistoryInline]

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('seeker', 'recruiter', 'scheduled_at', 'mode', 'status')
    list_filter = ('mode', 'status')
