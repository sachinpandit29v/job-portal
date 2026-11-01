from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Job, JobCategory, SavedJob, JobReport
from .forms import JobForm, JobReportForm
from recruiters.models import Company, RecruiterProfile
from applications.models import JobApplication

def job_list_view(request):
    jobs = Job.objects.filter(status='active').select_related('company', 'category', 'recruiter')

    # Keyword search
    q = request.GET.get('q', '').strip()
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(requirements__icontains=q) |
            Q(company__name__icontains=q)
        )

    # Location filter
    location = request.GET.get('location', '').strip()
    if location and location != 'all':
        jobs = jobs.filter(location__icontains=location)

    # Category filter
    category_slug = request.GET.get('category', '').strip()
    if category_slug and category_slug != 'all':
        jobs = jobs.filter(category__slug=category_slug)

    # Company filter
    company_slug = request.GET.get('company', '').strip()
    if company_slug and company_slug != 'all':
        jobs = jobs.filter(company__slug=company_slug)

    # Experience level filter
    experience = request.GET.get('experience_level', '').strip()
    if experience and experience != 'all':
        jobs = jobs.filter(experience_level=experience)

    # Employment type filter
    emp_type = request.GET.get('employment_type', '').strip()
    if emp_type and emp_type != 'all':
        jobs = jobs.filter(employment_type=emp_type)

    # Minimum salary
    min_salary = request.GET.get('min_salary', '').strip()
    if min_salary:
        try:
            jobs = jobs.filter(max_salary__gte=int(min_salary))
        except ValueError:
            pass

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'salary_high':
        jobs = jobs.order_by('-max_salary', '-created_at')
    elif sort == 'featured':
        jobs = jobs.order_by('-is_featured', '-created_at')
    elif sort == 'popular':
        jobs = jobs.order_by('-views_count', '-created_at')
    else:
        jobs = jobs.order_by('-created_at')

    # Pagination
    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    saved_job_ids = set()
    if request.user.is_authenticated and request.user.role == 'seeker':
        saved_job_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    categories = JobCategory.objects.all()
    companies = Company.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'companies': companies,
        'saved_job_ids': saved_job_ids,
        'selected_q': q,
        'selected_location': location,
        'selected_category': category_slug,
        'selected_company': company_slug,
        'selected_experience': experience,
        'selected_emp_type': emp_type,
        'selected_min_salary': min_salary,
        'selected_sort': sort,
        'total_jobs_count': jobs.count(),
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail_view(request, job_id):
    allowed_statuses = ['active']
    if request.user.is_authenticated and request.user.role == 'admin':
        allowed_statuses = ['active', 'closed', 'rejected']
    job = get_object_or_404(
        Job.objects.select_related('company', 'category', 'recruiter'),
        id=job_id,
        status__in=allowed_statuses,
    )

    # Increment views
    Job.objects.filter(id=job_id).update(views_count=job.views_count + 1)
    job.refresh_from_db()

    # Similar jobs
    similar_jobs = Job.objects.filter(category=job.category, status='active').exclude(id=job.id)[:3]

    # Application state for current user
    user_application = None
    is_saved = False
    if request.user.is_authenticated and request.user.role == 'seeker':
        user_application = JobApplication.objects.filter(job=job, seeker=request.user).first()
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()

    report_form = JobReportForm()

    context = {
        'job': job,
        'similar_jobs': similar_jobs,
        'user_application': user_application,
        'is_saved': is_saved,
        'report_form': report_form,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def post_job_view(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can publish vacancies.")
        return redirect('dashboard:index')

    recruiter_profile = get_object_or_404(RecruiterProfile, user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.company = recruiter_profile.company
            job.status = 'active'
            job.save()
            messages.success(request, f"Vacancy '{job.title}' published successfully!")
            return redirect('jobs:manage_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form, 'is_edit': False})

@login_required
def edit_job_view(request, job_id):
    if request.user.role != 'recruiter':
        messages.error(request, "Permission denied.")
        return redirect('dashboard:index')

    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vacancy '{job.title}' updated successfully.")
            return redirect('jobs:manage_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/post_job.html', {'form': form, 'job': job, 'is_edit': True})

@login_required
def delete_job_view(request, job_id):
    if request.user.role != 'recruiter':
        return redirect('dashboard:index')

    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    job.status = 'closed'
    job.save()
    messages.info(request, f"Job '{job.title}' has been closed.")
    return redirect('jobs:manage_jobs')

@login_required
def manage_jobs_view(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Access restricted to recruiters.")
        return redirect('dashboard:index')

    jobs = Job.objects.filter(recruiter=request.user).annotate(
        applicants_count=Count('applications')
    ).order_by('-created_at')

    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})

@login_required
def toggle_save_job_view(request, job_id):
    if request.user.role != 'seeker':
        return redirect('jobs:job_detail', job_id=job_id)

    job = get_object_or_404(Job, id=job_id)
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)

    if not created:
        saved.delete()
        messages.info(request, f"Removed '{job.title}' from your saved jobs.")
    else:
        messages.success(request, f"Saved '{job.title}' to your bookmarks.")

    next_url = request.META.get('HTTP_REFERER')
    return redirect(next_url or 'jobs:saved_jobs')

@login_required
def saved_jobs_view(request):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    saved_items = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company', 'job__category')
    return render(request, 'jobs/saved_jobs.html', {'saved_items': saved_items})

@login_required
def report_job_view(request, job_id):
    if request.user.role != 'seeker':
        messages.error(request, "Only job seekers can report job listings.")
        return redirect('jobs:job_detail', job_id=job_id)

    job = get_object_or_404(Job, id=job_id, status='active')
    if request.method == 'POST':
        form = JobReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.job = job
            report.reporter = request.user
            try:
                report.save()
            except IntegrityError:
                messages.info(request, "You have already reported this job listing.")
            else:
                messages.success(request, "Report submitted to platform moderation. Thank you for maintaining portal integrity.")
        else:
            messages.error(request, "Please provide a valid reason for the report.")
    return redirect('jobs:job_detail', job_id=job.id)
