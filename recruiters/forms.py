from django import forms
from .models import Company

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'website', 'location', 'industry', 'company_size', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'company_size': forms.Select(
                choices=[
                    ('1-20 employees', '1-20 employees'),
                    ('20-50 employees', '20-50 employees'),
                    ('50-100 employees', '50-100 employees'),
                    ('100-250 employees', '100-250 employees'),
                    ('250-500 employees', '250-500 employees'),
                    ('500+ employees', '500+ employees'),
                ],
                attrs={'class': 'form-select'}
            ),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
