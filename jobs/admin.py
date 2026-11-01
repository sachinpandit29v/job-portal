from django.contrib import admin
from .models import JobCategory, Job, SavedJob, JobReport, JobReportHistory

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'location', 'employment_type', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'employment_type', 'experience_level', 'is_featured', 'category')
    search_fields = ('title', 'description', 'requirements', 'company__name')

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_at')

@admin.register(JobReport)
class JobReportAdmin(admin.ModelAdmin):
    list_display = ('job', 'reporter', 'reason', 'status', 'created_at')


@admin.register(JobReportHistory)
class JobReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('report', 'previous_status', 'new_status', 'changed_by', 'created_at')
