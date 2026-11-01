from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import JobApplication, ApplicationStatusHistory, Interview
from .forms import ApplyJobForm, UpdateStatusForm
from jobs.models import Job
from notifications.models import Notification

@login_required
def apply_view(request, job_id):
    if request.user.role != 'seeker':
        messages.error(request, "Only job seekers can apply for open positions.")
        return redirect('jobs:job_detail', job_id=job_id)

    job = get_object_or_404(Job, id=job_id, status='active')

    # Check for duplicate application
    existing_app = JobApplication.objects.filter(job=job, seeker=request.user).first()
    if existing_app:
        messages.warning(request, f"You have already applied for this vacancy. Current status: '{existing_app.current_status}'.")
        return redirect('applications:tracking', application_id=existing_app.id)

    profile = getattr(request.user, 'seeker_profile', None)

    if request.method == 'POST':
        form = ApplyJobForm(request.POST, request.FILES)
        if form.is_valid():
            use_profile = form.cleaned_data.get('use_profile_resume')
            custom_file = form.cleaned_data.get('custom_resume_file')

            resume_filename = "Resume.pdf"
            resume_content = f"# {request.user.full_name}\nEmail: {request.user.email}"
            resume_file = None

            if not use_profile and custom_file:
                resume_file = custom_file
                resume_filename = custom_file.name
                resume_content = f"Uploaded resume file: {custom_file.name}"
            elif profile:
                resume_file = profile.resume
                resume_filename = profile.resume_filename or f"{request.user.full_name}_Resume.pdf"
                resume_content = profile.resume_content or f"# {request.user.full_name}\nEmail: {request.user.email}"

            try:
                application = JobApplication.objects.create(
                    job=job,
                    seeker=request.user,
                    resume_file=resume_file,
                    resume_filename=resume_filename,
                    resume_content=resume_content,
                    cover_letter=form.cleaned_data.get('cover_letter'),
                    current_status='Applied'
                )

                # Status History initial log
                ApplicationStatusHistory.objects.create(
                    application=application,
                    previous_status='Applied',
                    new_status='Applied',
                    changed_by=request.user,
                    remarks='Application submitted by candidate.'
                )

                # Notifications
                Notification.objects.create(
                    user=request.user,
                    title="Application Submitted",
                    message=f"Your application for '{job.title}' was successfully submitted.",
                    link=f"/applications/{application.id}/tracking/"
                )
                Notification.objects.create(
                    user=job.recruiter,
                    title="New Candidate Application",
                    message=f"{request.user.full_name} applied for '{job.title}'.",
                    link=f"/applications/recruiter/{application.id}/"
                )

                messages.success(request, f"Successfully submitted application for '{job.title}'!")
                return redirect('applications:tracking', application_id=application.id)
            except IntegrityError:
                messages.error(request, "Duplicate application detected. You have already applied for this job.")
                return redirect('jobs:job_detail', job_id=job.id)
    else:
        initial_cover = f"Dear Hiring Team at {job.company.name},\n\nI am thrilled to apply for the {job.title} position. My software engineering experience aligns directly with your technical expectations.\n\nBest regards,\n{request.user.full_name}"
        form = ApplyJobForm(initial={'cover_letter': initial_cover})

    return render(request, 'applications/apply.html', {'job': job, 'form': form, 'profile': profile})

@login_required
def my_applications_view(request):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    status_filter = request.GET.get('status', 'all')
    applications = JobApplication.objects.filter(seeker=request.user).select_related('job', 'job__company')

    if status_filter != 'all':
        applications = applications.filter(current_status=status_filter)

    return render(request, 'applications/my_applications.html', {
        'applications': applications,
        'selected_status': status_filter
    })

@login_required
def application_tracking_view(request, application_id):
    if request.user.role == 'seeker':
        application = get_object_or_404(JobApplication.objects.select_related('job', 'job__company'), id=application_id, seeker=request.user)
    elif request.user.role == 'recruiter':
        application = get_object_or_404(JobApplication.objects.select_related('job', 'job__company'), id=application_id, job__recruiter=request.user)
    elif request.user.role == 'admin':
        application = get_object_or_404(JobApplication.objects.select_related('job', 'job__company'), id=application_id)
    else:
        return redirect('dashboard:index')

    history = application.status_history.select_related('changed_by').order_by('created_at')
    interview = application.interviews.filter(status='Scheduled').first()

    stages = [
        {'key': 'Applied', 'label': 'Applied', 'desc': 'Application logged'},
        {'key': 'Under Review', 'label': 'Under Review', 'desc': 'Screening profile'},
        {'key': 'Shortlisted', 'label': 'Shortlisted', 'desc': 'Selected for panel'},
        {'key': 'Interview Scheduled', 'label': 'Interview', 'desc': 'Discussion confirmed'},
        {'key': 'Interview Completed', 'label': 'Interview Done', 'desc': 'Evaluation finished'},
        {'key': 'Selected', 'label': 'Offer / Selected', 'desc': 'Candidate offered'},
    ]

    stage_order = ['Applied', 'Under Review', 'Shortlisted', 'Interview Scheduled', 'Interview Completed', 'Selected']
    try:
        current_index = stage_order.index(application.current_status)
    except ValueError:
        current_index = -1

    return render(request, 'applications/application_tracking.html', {
        'application': application,
        'history': history,
        'interview': interview,
        'stages': stages,
        'current_index': current_index,
    })

@login_required
def withdraw_application_view(request, application_id):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    application = get_object_or_404(JobApplication, id=application_id, seeker=request.user)

    if application.current_status in ['Selected', 'Rejected', 'Withdrawn']:
        messages.warning(request, f"Cannot withdraw application that is already '{application.current_status}'.")
        return redirect('applications:tracking', application_id=application.id)

    prev_status = application.current_status
    application.current_status = 'Withdrawn'
    application.save()

    ApplicationStatusHistory.objects.create(
        application=application,
        previous_status=prev_status,
        new_status='Withdrawn',
        changed_by=request.user,
        remarks='Application voluntarily withdrawn by candidate.'
    )

    Notification.objects.create(
        user=request.user,
        title="Application Withdrawn",
        message=f"You withdrew your application for '{application.job.title}'.",
        link=f"/applications/{application.id}/tracking/"
    )

    messages.info(request, "Application has been withdrawn.")
    return redirect('applications:tracking', application_id=application.id)

@login_required
def recruiter_applicants_view(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Access restricted to recruiters.")
        return redirect('dashboard:index')

    job_id = request.GET.get('job_id', 'all')
    status_filter = request.GET.get('status', 'all')

    applicants = JobApplication.objects.filter(job__recruiter=request.user).select_related(
        'job', 'seeker', 'seeker__seeker_profile'
    )

    if job_id != 'all':
        applicants = applicants.filter(job_id=job_id)
    if status_filter != 'all':
        applicants = applicants.filter(current_status=status_filter)

    recruiter_jobs = Job.objects.filter(recruiter=request.user)

    return render(request, 'applications/recruiter_applicants.html', {
        'applicants': applicants,
        'recruiter_jobs': recruiter_jobs,
        'selected_job_id': job_id,
        'selected_status': status_filter,
    })

@login_required
def applicant_detail_view(request, application_id):
    if request.user.role != 'recruiter':
        messages.error(request, "Access restricted.")
        return redirect('dashboard:index')

    application = get_object_or_404(
        JobApplication.objects.select_related('job', 'seeker', 'seeker__seeker_profile'),
        id=application_id,
        job__recruiter=request.user
    )

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            remarks = form.cleaned_data.get('remarks') or f"Status updated to {new_status}"
            rec_notes = form.cleaned_data.get('recruiter_notes')
            int_date = form.cleaned_data.get('interview_date')
            int_link = form.cleaned_data.get('interview_link')

            prev_status = application.current_status
            application.current_status = new_status
            if rec_notes:
                application.recruiter_notes = rec_notes
            if int_date:
                application.interview_date = int_date
            if int_link:
                application.interview_link = int_link
            application.save()

            ApplicationStatusHistory.objects.create(
                application=application,
                previous_status=prev_status,
                new_status=new_status,
                changed_by=request.user,
                remarks=remarks
            )

            # In-app notification for candidate
            Notification.objects.create(
                user=application.seeker,
                title=f"Application Stage: {new_status}",
                message=f"Your application for '{application.job.title}' is now '{new_status}'. {remarks}",
                link=f"/applications/{application.id}/tracking/"
            )

            # Schedule interview model record if applicable
            if new_status == 'Interview Scheduled' and int_date:
                Interview.objects.create(
                    application=application,
                    recruiter=request.user,
                    seeker=application.seeker,
                    scheduled_at=int_date,
                    meeting_link=int_link,
                    notes=remarks,
                    status='Scheduled'
                )

            messages.success(request, f"Updated application status to '{new_status}'.")
            return redirect('applications:applicant_detail', application_id=application.id)
    else:
        form = UpdateStatusForm(initial={
            'status': application.current_status,
            'recruiter_notes': application.recruiter_notes,
            'interview_date': application.interview_date,
            'interview_link': application.interview_link,
        })

    history = application.status_history.select_related('changed_by').order_by('created_at')

    return render(request, 'applications/applicant_detail.html', {
        'application': application,
        'form': form,
        'history': history,
    })
