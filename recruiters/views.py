from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, RecruiterProfile
from .forms import CompanyProfileForm

@login_required
def company_profile_view(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can manage company profiles.")
        return redirect('dashboard:index')

    recruiter_profile = get_object_or_404(RecruiterProfile, user=request.user)
    company = recruiter_profile.company

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated successfully!")
            return redirect('recruiters:company_profile')
    else:
        form = CompanyProfileForm(instance=company)

    return render(request, 'recruiters/company_profile.html', {
        'form': form,
        'company': company,
        'recruiter_profile': recruiter_profile
    })
