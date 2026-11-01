from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='companies/', blank=True, null=True)
    logo_initials = models.CharField(max_length=5, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=150)
    company_size = models.CharField(max_length=50, default='100-250 employees')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.logo_initials:
            self.logo_initials = (self.name[:2]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='recruiters')
    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=150, blank=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.company.name})"
