from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, JobSeekerProfile
from recruiters.models import Company, RecruiterProfile
from jobs.models import JobCategory, Job
from applications.models import JobApplication, ApplicationStatusHistory

class JobPortalTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Admin
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com', password='password123', full_name='Admin Test', role='admin'
        )

        # Recruiter
        self.recruiter_user = User.objects.create_user(
            email='recruiter@test.com', password='password123', full_name='Recruiter Test', role='recruiter'
        )
        self.company = Company.objects.create(name='Test Corp', location='San Francisco, CA')
        self.recruiter_profile = RecruiterProfile.objects.create(
            user=self.recruiter_user, company=self.company, designation='Recruiter'
        )

        # Seeker
        self.seeker_user = User.objects.create_user(
            email='seeker@test.com', password='password123', full_name='Seeker Test', role='seeker'
        )
        self.seeker_profile = JobSeekerProfile.objects.create(
            user=self.seeker_user, headline='Junior Engineer', education='B.S. CS'
        )

        # Category and Job
        self.category = JobCategory.objects.create(name='Engineering', slug='engineering')
        self.job = Job.objects.create(
            recruiter=self.recruiter_user,
            company=self.company,
            category=self.category,
            title='Software Developer',
            slug='software-developer',
            location='Remote',
            employment_type='Full-Time',
            experience_level='Fresher / Entry',
            min_salary=70000,
            max_salary=90000,
            description='Test description',
            requirements='Test requirements',
            responsibilities='Test responsibilities'
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Portal')

    def test_job_list_loads(self):
        response = self.client.get(reverse('jobs:job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')

    def test_job_detail_loads(self):
        response = self.client.get(reverse('jobs:job_detail', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')
        self.assertContains(response, 'Test Corp')

    def test_seeker_apply_job_and_duplicate_prevention(self):
        self.client.login(email='seeker@test.com', password='password123')
        
        # Apply
        response = self.client.post(reverse('applications:apply', args=[self.job.id]), {
            'use_profile_resume': True,
            'cover_letter': 'Excited to apply for this role!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JobApplication.objects.filter(seeker=self.seeker_user, job=self.job).exists())
        
        # Verify ATS status history was logged
        app = JobApplication.objects.get(seeker=self.seeker_user, job=self.job)
        self.assertEqual(app.current_status, 'Applied')
        self.assertTrue(ApplicationStatusHistory.objects.filter(application=app).exists())

        # Attempt duplicate application
        dup_response = self.client.post(reverse('applications:apply', args=[self.job.id]), {
            'use_profile_resume': True,
            'cover_letter': 'Duplicate attempt'
        }, follow=True)
        # Should redirect to tracking and prevent duplicate creation
        self.assertEqual(JobApplication.objects.filter(seeker=self.seeker_user, job=self.job).count(), 1)

    def test_recruiter_status_update(self):
        # Create application first
        app = JobApplication.objects.create(
            job=self.job,
            seeker=self.seeker_user,
            current_status='Applied'
        )
        
        self.client.login(email='recruiter@test.com', password='password123')
        response = self.client.post(reverse('applications:applicant_detail', args=[app.id]), {
            'status': 'Shortlisted',
            'remarks': 'Candidate shortlisted after technical review.'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.current_status, 'Shortlisted')
        self.assertTrue(ApplicationStatusHistory.objects.filter(application=app, new_status='Shortlisted').exists())

    def test_admin_dashboard_access(self):
        # Seeker cannot access admin dashboard
        self.client.login(email='seeker@test.com', password='password123')
        response = self.client.get(reverse('dashboard:admin'), follow=True)
        self.assertNotEqual(response.status_code, 403)
        # Redirected because role != admin
        
        # Admin can access
        self.client.login(email='admin@test.com', password='password123')
        admin_response = self.client.get(reverse('dashboard:admin'))
        self.assertEqual(admin_response.status_code, 200)
        self.assertContains(admin_response, 'Platform Administration')
