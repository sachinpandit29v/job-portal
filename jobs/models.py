from django.db import models
from django.conf import settings
from django.utils.text import slugify
from recruiters.models import Company

class JobCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='briefcase')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Job Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    EMPLOYMENT_TYPES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    )
    EXPERIENCE_LEVELS = (
        ('Fresher / Entry', 'Fresher / Entry (0-2 years)'),
        ('Mid-Level', 'Mid-Level (2-5 years)'),
        ('Senior', 'Senior (5+ years)'),
        ('Lead / Executive', 'Lead / Executive'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    )

    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, related_name='jobs')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    benefits = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=30, choices=EMPLOYMENT_TYPES, default='Full-Time')
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_LEVELS, default='Mid-Level')
    min_salary = models.PositiveIntegerField(null=True, blank=True)
    max_salary = models.PositiveIntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='active')
    views_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"


class JobReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('dismissed', 'Dismissed'),
        ('resolved', 'Resolved'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_submitted')
    reason = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['job', 'reporter'], name='unique_job_reporter_report'),
        ]

    def __str__(self):
        return f"Report on {self.job.title} by {self.reporter.email}"


class JobReportHistory(models.Model):
    report = models.ForeignKey(JobReport, on_delete=models.CASCADE, related_name='moderation_history')
    previous_status = models.CharField(max_length=25)
    new_status = models.CharField(max_length=25)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='job_report_moderation_actions',
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
