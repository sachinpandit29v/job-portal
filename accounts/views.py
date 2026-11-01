from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import User, JobSeekerProfile
from .forms import (
    LoginForm, JobSeekerRegistrationForm, RecruiterRegistrationForm,
    JobSeekerProfileForm, ResumeUploadForm
)
from recruiters.models import Company, RecruiterProfile
from notifications.models import Notification

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.user)
        messages.success(request, f"Welcome back, {form.user.full_name}!")
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('dashboard:index')

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:home')

def register_seeker_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = JobSeekerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'seeker'
        user.set_password(form.cleaned_data['password'])
        user.save()

        JobSeekerProfile.objects.create(
            user=user,
            headline=form.cleaned_data.get('headline', 'Aspiring Professional')
        )

        Notification.objects.create(
            user=user,
            title="Welcome to Job Portal & ATS!",
            message="Your candidate account was created. Upload your resume and browse verified vacancies.",
            link="/dashboard/"
        )

        login(request, user)
        messages.success(request, "Registration successful! Welcome to your candidate portal.")
        return redirect('dashboard:index')

    return render(request, 'accounts/register.html', {'form': form, 'role_type': 'seeker'})

def register_recruiter_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = RecruiterRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'recruiter'
        user.set_password(form.cleaned_data['password'])
        user.save()

        comp_name = form.cleaned_data['company_name']
        slug = slugify(comp_name)
        company, _ = Company.objects.get_or_create(
            slug=slug,
            defaults={'name': comp_name, 'location': 'Remote', 'industry': 'Technology'}
        )

        RecruiterProfile.objects.create(
            user=user,
            company=company,
            designation=form.cleaned_data['designation']
        )

        login(request, user)
        messages.success(request, "Recruiter registration complete! You can now publish job vacancies.")
        return redirect('dashboard:index')

    return render(request, 'accounts/register.html', {'form': form, 'role_type': 'recruiter'})

@login_required
def profile_view(request):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            request.user.full_name = form.cleaned_data['full_name']
            request.user.phone = form.cleaned_data['phone']
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        initial = {'full_name': request.user.full_name, 'phone': request.user.phone}
        form = JobSeekerProfileForm(instance=profile, initial=initial)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

@login_required
def resume_upload_view(request):
    if request.user.role != 'seeker':
        return redirect('dashboard:index')

    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data.get('resume_file')
            text = form.cleaned_data.get('resume_text')
            if f:
                profile.resume = f
                profile.resume_filename = f.name
            if text:
                profile.resume_content = text
            profile.save()
            messages.success(request, "Resume saved to your candidate profile.")
            return redirect('accounts:resume')
    else:
        form = ResumeUploadForm(initial={'resume_text': profile.resume_content})

    return render(request, 'accounts/resume_upload.html', {'form': form, 'profile': profile})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_p = request.POST.get('old_password')
        new_p = request.POST.get('new_password')
        confirm_p = request.POST.get('confirm_password')

        if not request.user.check_password(old_p):
            messages.error(request, "Current password does not match.")
        elif new_p != confirm_p:
            messages.error(request, "New passwords do not match.")
        elif len(new_p) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            request.user.set_password(new_p)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully!")
            return redirect('accounts:change_password')

    return render(request, 'accounts/change_password.html')
