from django.shortcuts import render
from django.db.models import Count, Q
from jobs.models import Job, JobCategory
from recruiters.models import Company
from accounts.models import User
from applications.models import JobApplication
from .models import ContactMessage

def home_view(request):
    featured_jobs = Job.objects.filter(status='active', is_featured=True).select_related('company', 'category')[:6]
    recent_jobs = Job.objects.filter(status='active').select_related('company', 'category').order_by('-created_at')[:6]
    categories = JobCategory.objects.annotate(
        active_jobs_count=Count('jobs', filter=Q(jobs__status='active'))
    ).order_by('-active_jobs_count')[:8]
    companies = Company.objects.annotate(
        open_positions=Count('jobs', filter=Q(jobs__status='active'))
    ).order_by('-open_positions')[:4]

    stats = {
        'total_jobs': Job.objects.filter(status='active').count(),
        'total_companies': Company.objects.count(),
        'total_seekers': User.objects.filter(role='seeker').count(),
        'total_applications': JobApplication.objects.count(),
    }

    context = {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'categories': categories,
        'companies': companies,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            subject=request.POST.get('subject', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        return render(request, 'core/contact.html', {'message_sent': True})
    return render(request, 'core/contact.html')
