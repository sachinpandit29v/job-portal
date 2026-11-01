from django import forms
from .models import Job, JobReport, JobCategory

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'location', 'employment_type', 'experience_level',
            'min_salary', 'max_salary', 'deadline', 'is_featured',
            'description', 'requirements', 'responsibilities'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Junior Full Stack Developer'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. San Francisco, CA or Remote'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70000'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '95000'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class JobReportForm(forms.ModelForm):
    class Meta:
        model = JobReport
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(
                choices=[
                    ('', 'Select a reason...'),
                    ('Fake Job Posting', 'Fake Job Posting'),
                    ('Misleading Job Description', 'Misleading Job Description'),
                    ('Fraudulent Recruitment', 'Fraudulent Recruitment'),
                    ('Incorrect Salary Information', 'Incorrect Salary Information'),
                    ('Expired Job Vacancy', 'Expired Job Vacancy'),
                    ('Suspicious Company', 'Suspicious Company'),
                    ('Other', 'Other'),
                ],
                attrs={'class': 'form-select'}
            ),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Provide additional details for moderation audit...'}),
        }
