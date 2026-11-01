from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Q, Prefetch
from accounts.models import User, JobSeekerProfile
from jobs.models import Job, JobCategory, SavedJob, JobReport
from applications.models import JobApplication, Interview
from recruiters.models import Company, RecruiterProfile
from notifications.models import Notification
from jobs.models import JobReportHistory
from core.models import ContactMessage
from .forms import AdminCategoryForm

@login_required
def index_view(request):
    if request.user.role == 'seeker':
        return redirect('dashboard:seeker')
    elif request.user.role == 'recruiter':
        return redirect('dashboard:recruiter')
    elif request.user.role == 'admin':
        return redirect('dashboard:admin')
    return redirect('core:home')

@login_required
def seeker_dashboard_view(request):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    apps = JobApplication.objects.filter(seeker=request.user)
    stats = {
        'total': apps.count(),
        'under_review': apps.filter(current_status='Under Review').count(),
        'shortlisted': apps.filter(current_status='Shortlisted').count(),
        'interviews': apps.filter(current_status__in=['Interview Scheduled', 'Interview Completed']).count(),
        'selected': apps.filter(current_status='Selected').count(),
        'saved': SavedJob.objects.filter(user=request.user).count(),
    }

    recent_applications = apps.select_related('job', 'job__company').order_by('-updated_at')[:5]
    upcoming_interviews = Interview.objects.filter(seeker=request.user, status='Scheduled').select_related(
        'application__job', 'application__job__company', 'recruiter'
    ).order_by('scheduled_at')[:4]

    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    # Profile strength calculation
    checklist = [
        bool(request.user.full_name and request.user.phone),
        bool(profile.headline),
        bool(profile.education),
        bool(profile.skills),
        bool(profile.resume_filename or profile.resume),
        bool(profile.github_url or profile.portfolio_url),
    ]
    strength_pct = int((sum(checklist) / len(checklist)) * 100)

    context = {
        'stats': stats,
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
        'profile': profile,
        'strength_pct': strength_pct,
    }
    return render(request, 'dashboard/seeker_dashboard.html', context)

@login_required
def recruiter_dashboard_view(request):
    if request.user.role != 'recruiter':
        return redirect('dashboard:index')

    recruiter_jobs = Job.objects.filter(recruiter=request.user)
    recruiter_apps = JobApplication.objects.filter(job__recruiter=request.user)

    job_stats = recruiter_jobs.aggregate(
        active_jobs=Count('id', filter=Q(status='active')),
    )
    applicant_stats = recruiter_apps.aggregate(
        total_applicants=Count('id'),
        under_review=Count('id', filter=Q(current_status='Under Review')),
        shortlisted=Count('id', filter=Q(current_status='Shortlisted')),
        interviews_scheduled=Count('id', filter=Q(current_status='Interview Scheduled')),
    )
    stats = {**job_stats, **applicant_stats}

    recent_applicants = recruiter_apps.select_related(
        'job', 'seeker', 'seeker__seeker_profile'
    ).order_by('-created_at', '-id')[:5]
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    context = {
        'stats': stats,
        'recent_applicants': recent_applicants,
        'company': recruiter_profile.company if recruiter_profile else None,
    }
    return render(request, 'dashboard/recruiter_dashboard.html', context)

@login_required
def recruiter_analytics_view(request):
    if request.user.role != 'recruiter':
        return redirect('dashboard:index')

    recruiter_applications = JobApplication.objects.filter(job__recruiter=request.user)
    application_counts = dict(
        recruiter_applications.values('current_status')
        .annotate(count=Count('id'))
        .values_list('current_status', 'count')
    )
    status_counts = [
        {
            'value': status_value,
            'label': status_label if status_value != 'Selected' else 'Selected',
            'count': application_counts.get(status_value, 0),
        }
        for status_value, status_label in JobApplication.STATUS_CHOICES
    ]

    jobs_breakdown = list(
        Job.objects.filter(recruiter=request.user)
        .annotate(app_count=Count('applications'))
        .order_by('-app_count', 'title')
        .values('title', 'app_count')
    )

    context = {
        'status_counts': status_counts,
        'jobs_breakdown': jobs_breakdown,
        'total_applications': recruiter_applications.count(),
    }
    return render(request, 'dashboard/recruiter_analytics.html', context)

@login_required
def admin_dashboard_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access restricted to administrators.")
        return redirect('dashboard:index')

    seeker_query = request.GET.get('seeker_q', '').strip()
    seeker_status = request.GET.get('seeker_status', 'all')
    recruiter_query = request.GET.get('recruiter_q', '').strip()
    recruiter_status = request.GET.get('recruiter_status', 'all')

    seekers = User.objects.filter(role='seeker').order_by('-created_at')
    if seeker_query:
        seekers = seekers.filter(Q(full_name__icontains=seeker_query) | Q(email__icontains=seeker_query))
    if seeker_status in ('active', 'inactive'):
        seekers = seekers.filter(is_active=seeker_status == 'active')
    seeker_page = Paginator(seekers, 10).get_page(request.GET.get('seeker_page'))

    recruiters = RecruiterProfile.objects.filter(user__role='recruiter').select_related(
        'user', 'company'
    ).annotate(
        total_jobs=Count('user__posted_jobs', distinct=True),
        active_jobs=Count('user__posted_jobs', filter=Q(user__posted_jobs__status='active'), distinct=True),
        closed_jobs=Count('user__posted_jobs', filter=Q(user__posted_jobs__status='closed'), distinct=True),
        total_applications=Count('user__posted_jobs__applications', distinct=True),
    ).prefetch_related(
        Prefetch(
            'user__posted_jobs',
            queryset=Job.objects.annotate(application_count=Count('applications')).order_by('-created_at'),
            to_attr='admin_posted_jobs',
        )
    ).order_by('-created_at')
    if recruiter_query:
        recruiters = recruiters.filter(
            Q(user__full_name__icontains=recruiter_query)
            | Q(user__email__icontains=recruiter_query)
            | Q(company__name__icontains=recruiter_query)
        )
    if recruiter_status in ('active', 'inactive'):
        recruiters = recruiters.filter(user__is_active=recruiter_status == 'active')
    recruiter_page = Paginator(recruiters, 10).get_page(request.GET.get('recruiter_page'))

    report_query = request.GET.get('report_q', '').strip()
    report_status = request.GET.get('report_status', 'all')
    reports = JobReport.objects.all().select_related(
        'job', 'job__company', 'job__recruiter', 'reporter'
    ).prefetch_related('moderation_history').order_by('-created_at')
    if report_query:
        reports = reports.filter(
            Q(job__title__icontains=report_query)
            | Q(job__company__name__icontains=report_query)
            | Q(job__recruiter__full_name__icontains=report_query)
        )
    if report_status in ('pending', 'under_review', 'resolved', 'dismissed'):
        reports = reports.filter(status=report_status)
    report_page = Paginator(reports, 10).get_page(request.GET.get('report_page'))

    category_query = request.GET.get('category_q', '').strip()
    categories_queryset = JobCategory.objects.annotate(job_count=Count('jobs')).order_by('name')
    if category_query:
        categories_queryset = categories_queryset.filter(
            Q(name__icontains=category_query) | Q(description__icontains=category_query)
        )
    category_page = Paginator(categories_queryset, 12).get_page(request.GET.get('category_page'))
    contact_messages = ContactMessage.objects.all()[:25]

    pagination_queries = {}
    for page_param in ('seeker_page', 'recruiter_page', 'report_page', 'category_page'):
        query_params = request.GET.copy()
        query_params.pop(page_param, None)
        pagination_queries[page_param] = query_params.urlencode()

    stats = {
        'total_users': User.objects.filter(role__in=['seeker', 'recruiter']).count(),
        'total_seekers': User.objects.filter(role='seeker').count(),
        'total_recruiters': User.objects.filter(role='recruiter').count(),
        'active_seekers': User.objects.filter(role='seeker', is_active=True).count(),
        'active_recruiters': User.objects.filter(role='recruiter', is_active=True).count(),
        'active_jobs': Job.objects.filter(status='active').count(),
        'total_applications': JobApplication.objects.count(),
        'pending_reports': JobReport.objects.filter(status__in=['pending', 'under_review']).count(),
    }

    application_counts = dict(
        JobApplication.objects.values('current_status').annotate(count=Count('id')).values_list(
            'current_status', 'count'
        )
    )
    status_chart = [
        {'label': label, 'count': application_counts.get(value, 0)}
        for value, label in JobApplication.STATUS_CHOICES
    ]
    category_chart = list(
        JobCategory.objects.annotate(count=Count('jobs')).order_by('name').values('name', 'count')
    )

    context = {
        'stats': stats,
        'seeker_page': seeker_page,
        'recruiter_page': recruiter_page,
        'seeker_query': seeker_query,
        'seeker_status': seeker_status,
        'recruiter_query': recruiter_query,
        'recruiter_status': recruiter_status,
        'report_page': report_page,
        'report_query': report_query,
        'report_status': report_status,
        'category_page': category_page,
        'contact_messages': contact_messages,
        'category_query': category_query,
        'pagination_queries': pagination_queries,
        'category_form': AdminCategoryForm(),
        'status_chart': status_chart,
        'category_chart': category_chart,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def admin_toggle_user_view(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard:index')
    if request.method != 'POST':
        messages.error(request, "Account status changes must be submitted securely.")
        return redirect('dashboard:admin')

    target_user = get_object_or_404(User, id=user_id)
    if target_user.role not in ('seeker', 'recruiter'):
        messages.error(request, "Only seeker and recruiter accounts can be managed here.")
    elif target_user.is_active and target_user.is_superuser and User.objects.filter(
        is_superuser=True, is_active=True
    ).count() <= 1:
        messages.error(request, "Cannot deactivate the last active superuser.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save()
        status_word = "Activated" if target_user.is_active else "Deactivated"
        messages.success(request, f"User {target_user.full_name} is now {status_word}.")

    return redirect('dashboard:admin')


@login_required
def admin_category_add_view(request):
    if request.user.role != 'admin':
        return redirect('dashboard:index')
    if request.method != 'POST':
        return redirect('dashboard:admin')
    form = AdminCategoryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Job category added.")
    else:
        messages.error(request, "Please correct the category details.")
    return redirect('dashboard:admin')


@login_required
def admin_category_action_view(request, category_id, action):
    if request.user.role != 'admin':
        return redirect('dashboard:index')
    if request.method != 'POST':
        messages.error(request, "Category changes must be submitted securely.")
        return redirect('dashboard:admin')

    category = get_object_or_404(JobCategory, id=category_id)
    if action == 'edit':
        form = AdminCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Job category updated.")
        else:
            messages.error(request, "Please correct the category details.")
    elif action == 'delete':
        try:
            category.delete()
        except IntegrityError:
            messages.error(request, "This category cannot be deleted while jobs use it.")
        else:
            messages.success(request, "Job category deleted.")
    return redirect('dashboard:admin')

@login_required
def admin_report_action_view(request, report_id, action):
    if request.user.role != 'admin':
        return redirect('dashboard:index')

    if request.method != 'POST':
        messages.error(request, "Report moderation actions must be submitted securely.")
        return redirect('dashboard:admin')

    report = get_object_or_404(JobReport.objects.select_related('job', 'job__recruiter', 'reporter'), id=report_id)
    if report.status in ('resolved', 'dismissed'):
        messages.info(request, "This report has already been reviewed.")
        return redirect('dashboard:admin')

    previous_status = report.status
    if action == 'under_review':
        report.status = 'under_review'
        report.save(update_fields=['status'])
        JobReportHistory.objects.create(
            report=report,
            previous_status=previous_status,
            new_status=report.status,
            changed_by=request.user,
            notes='Report assigned for administrator investigation.',
        )
        messages.info(request, "Report marked as under review.")
    elif action == 'dismiss':
        report.status = 'dismissed'
        report.save()
        JobReportHistory.objects.create(
            report=report,
            previous_status=previous_status,
            new_status=report.status,
            changed_by=request.user,
            notes='Report dismissed as invalid.',
        )
        Notification.objects.create(
            user=report.reporter,
            title='Job report reviewed',
            message=f"Your report about '{report.job.title}' was reviewed and dismissed.",
            link=f'/jobs/{report.job_id}/',
            type='system',
        )
        messages.info(request, "Report dismissed and the reporting user was notified.")
    elif action == 'resolve':
        report.status = 'resolved'
        report.save()
        JobReportHistory.objects.create(
            report=report,
            previous_status=previous_status,
            new_status=report.status,
            changed_by=request.user,
            notes='Report reviewed and resolved without removing the job.',
        )
        Notification.objects.create(
            user=report.reporter,
            title='Job report resolved',
            message=f"Your report about '{report.job.title}' was reviewed and resolved.",
            link=f'/jobs/{report.job_id}/',
            type='system',
        )
        messages.success(request, "Report marked as resolved and the reporting user was notified.")
    elif action == 'remove_job':
        report.status = 'resolved'
        report.save()
        report.job.status = 'rejected'
        report.job.save()
        JobReportHistory.objects.create(
            report=report,
            previous_status=previous_status,
            new_status=report.status,
            changed_by=request.user,
            notes='Job removed after moderation review.',
        )
        Notification.objects.create(
            user=report.reporter,
            title='Job report reviewed',
            message=f"Your report about '{report.job.title}' was reviewed and the listing was removed.",
            link='/jobs/',
            type='system',
        )
        Notification.objects.create(
            user=report.job.recruiter,
            title='Job listing removed',
            message=f"Your job listing '{report.job.title}' was removed after a moderation review.",
            link='/dashboard/recruiter/',
            type='system',
        )
        messages.warning(request, f"Job '{report.job.title}' removed and notifications sent.")

    return redirect('dashboard:admin')
