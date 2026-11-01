# Project Specification

## 1. Objective

JobPortalATS is a responsive Django application that connects job seekers and recruiters through a transparent application-tracking workflow, with administrative moderation and platform oversight.

## 2. Roles and requirements

### Job seeker
- Register and authenticate with a unique email address.
- Maintain profile, resume, skills, education, experience, and portfolio links.
- Browse active jobs with search, filters, sorting, salary ranges, and saved jobs.
- Submit one application per job with a resume and optional cover letter.
- Track status, remarks, interview details, and audit history.
- Withdraw applications where allowed.
- Read and mark notifications as read.

### Recruiter
- Register with company information and recruiter profile.
- Create, edit, close, and delete owned jobs.
- View only applications for owned jobs.
- Review candidate details, resume information, and cover letters.
- Update ATS status, add private notes, publish candidate-facing remarks, and schedule interviews.
- View recruiter-scoped dashboard statistics and Chart.js analytics.

### Administrator
- Access the admin dashboard and Django Admin.
- Manage seeker and recruiter account activation.
- Manage job categories.
- Review job reports and moderation history.
- Review contact messages.
- View platform-level statistics.

## 3. Functional requirements

| ID | Module | Requirement | Verification |
|---|---|---|---|
| FR-01 | Accounts | Unique email registration and role-aware authentication | Django tests and login verification |
| FR-02 | Profiles | Seeker resume/profile and recruiter company management | Form and route verification |
| FR-03 | Jobs | Search, filtering, sorting, saved jobs, and recruiter job management | Query and view tests |
| FR-04 | Applications | One application per seeker per job | Database unique constraint |
| FR-05 | ATS | Status updates create history and candidate notifications | Model and view verification |
| FR-06 | Interviews | Recruiters can schedule interviews with date and meeting link | Persistence verification |
| FR-07 | Analytics | Recruiter-scoped status and job aggregates | Django ORM aggregate queries |
| FR-08 | Administration | User, category, report, and contact-message management | Admin dashboard verification |
| FR-09 | Notifications | User-scoped list, mark-read, and mark-all-read actions | Route and database verification |
| FR-10 | Presentation | Responsive Bootstrap pages and LPA salary formatting | Template and browser verification |

## 4. Security requirements

- Use Django authentication, CSRF protection, password hashing, and permission checks.
- Scope recruiter data by `job__recruiter=request.user`.
- Scope seeker data by `seeker=request.user`.
- Scope notifications by `user=request.user`.
- Validate uploaded resume extensions and file size through forms.
- Use Django ORM queries rather than string-built SQL.
- Keep secrets out of source control.

## 5. Non-functional requirements

- Responsive Bootstrap 5 presentation for desktop and mobile.
- Clear empty states and user-facing feedback messages.
- SQLite is supported for local development; production deployments should use persistent storage and backups.
- Migrations must be applied before running the application.
