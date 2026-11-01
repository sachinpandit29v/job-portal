from django.db import models
from django.conf import settings
from jobs.models import Job

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Interview Completed', 'Interview Completed'),
        ('Selected', 'Selected / Offer'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume_file = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    resume_filename = models.CharField(max_length=255)
    resume_content = models.TextField()
    cover_letter = models.TextField(blank=True, null=True)
    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Applied')
    recruiter_notes = models.TextField(blank=True, null=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'seeker')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.seeker.full_name} -> {self.job.title} [{self.current_status}]"


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"App #{self.application_id}: {self.previous_status} -> {self.new_status}"


class Interview(models.Model):
    MODE_CHOICES = (
        ('Video Call', 'Video Call'),
        ('In-Person', 'In-Person'),
        ('Phone Screen', 'Phone Screen'),
    )
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviews_conducted')
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviews_attended')
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=45)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Video Call')
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview for {self.seeker.full_name} on {self.scheduled_at}"
