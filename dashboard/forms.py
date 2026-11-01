from django import forms
from jobs.models import JobCategory


class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Science'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
