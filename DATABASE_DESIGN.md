# Database Design

## Overview

The project uses Django models backed by SQLite during local development. Django manages schema creation through migrations. Authentication uses one custom `accounts.User` table with a `role` field; role-specific information is stored in related profile tables.

## Main relationships

```text
User 1--1 JobSeekerProfile
User 1--1 RecruiterProfile *--1 Company
User 1--* Job
JobCategory 1--* Job
Job 1--* JobApplication
User 1--* JobApplication
JobApplication 1--* ApplicationStatusHistory
JobApplication 1--* Interview
User 1--* Notification
User *--* Job through SavedJob
Job 1--* JobReport 1--* JobReportHistory
```

## Tables and important fields

### `accounts_user`
Custom Django authentication table. Stores email, password hash, full name, phone, avatar, role (`seeker`, `recruiter`, or `admin`), active status, staff flags, and timestamps.

### `accounts_jobseekerprofile`
One-to-one with a seeker user. Stores headline, bio, education, skills, experience, location, social links, resume file, resume filename, and text representation.

### `recruiters_company`
Stores company name, slug, logo, website, location, industry, company size, description, and creation time.

### `recruiters_recruiterprofile`
One-to-one with a recruiter user and foreign key to a company. Stores designation, department, verification status, and timestamps.

### `jobs_jobcategory`
Stores unique category names, slugs, icons, descriptions, and timestamps.

### `jobs_job`
Stores recruiter and company ownership, category, title, description, requirements, responsibilities, benefits, location, employment type, experience level, salary range, status, views, featured flag, deadline, and timestamps.

### `jobs_savedjob`
Connects a user to a saved job. The `(user, job)` pair is unique.

### `jobs_jobreport` and `jobs_jobreporthistory`
Store user-submitted job reports and administrator moderation history.

### `applications_jobapplication`
Stores job, seeker, uploaded resume, resume text, cover letter, current status, recruiter notes, interview fields, and timestamps. The `(job, seeker)` pair is unique to prevent duplicate applications.

### `applications_applicationstatushistory`
Stores every status transition, actor, candidate-facing remarks, and timestamp.

### `applications_interview`
Stores application, recruiter, seeker, scheduled time, duration, mode, meeting link, notes, status, and creation time.

### `notifications_notification`
Stores recipient, title, message, optional internal link, type, read flag, and timestamp. Notifications are scoped to the logged-in user.

### `core_contactmessage`
Stores public contact form submissions: sender name, email, subject, message, and timestamp. Administrators can review these messages.

### Django framework tables

The database also contains standard Django tables for migrations, sessions, permissions, groups, and admin log entries.

## Integrity and access rules

1. User email addresses are unique.
2. Seeker and recruiter profiles use one-to-one user relationships.
3. Duplicate saved jobs and applications are prevented by database constraints.
4. Deleting a user cascades to dependent records where configured.
5. Recruiter queries filter jobs and applications by `job__recruiter=request.user`.
6. Seeker queries filter applications and saved jobs by `request.user`.
7. Notification queries filter by `user=request.user`.
8. Django migrations are the source of truth for schema changes.
