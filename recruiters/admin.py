from django.contrib import admin
from .models import Company, RecruiterProfile

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'company_size')
    search_fields = ('name', 'industry', 'location')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'designation', 'is_verified')
    list_filter = ('is_verified', 'company')
