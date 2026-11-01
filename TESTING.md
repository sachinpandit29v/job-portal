# Testing and Verification

## Commands

Run from the project root:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

## Current result

- Django system checks: passed with no issues.
- Test suite: 6 tests passed.

## Verified workflows

| ID | Workflow | Result |
|---|---|---|
| TC-01 | Recruiter job ownership and job management | Passed |
| TC-02 | Recruiter applicant access and status update | Passed |
| TC-03 | Seeker application and duplicate prevention | Passed |
| TC-04 | Seeker application tracking and withdrawal | Passed |
| TC-05 | Admin dashboard access and role filtering | Passed |
| TC-06 | Job report moderation and permission checks | Passed |

## Additional manual verification

- Public home, About, Contact, login, and Browse Jobs pages return successfully.
- Recruiter dashboard, analytics, Manage Jobs, Candidate ATS, and applicant detail pages return successfully.
- Recruiter statistics and analytics use recruiter-owned jobs and applications only.
- Recent recruiter applications are limited to five and ordered newest first.
- Notification list loads, mark-as-read updates the notification, and mark-all-as-read updates unread records.
- Admin total registered users counts seekers and recruiters, excluding administrator accounts.
- LPA formatting converts stored annual values such as `1200000` to `₹12 LPA`.
- Responsive navbar shows role-appropriate links.

## Recommended production checks

Before deployment:

1. Run migrations against the production database.
2. Configure `DEBUG=False`, a secure secret key, and restricted allowed hosts.
3. Verify static and media storage.
4. Test login, role isolation, file uploads, and backups.
5. Run the full test suite in the deployment environment.
