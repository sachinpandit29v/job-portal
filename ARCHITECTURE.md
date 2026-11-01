# Architecture Specification: Job Portal & Application Tracking System

## 1. System Topology & Tier Architecture

The application uses Django's server-rendered architecture with Bootstrap presentation, Django business logic, and SQLite persistence:

```
+-------------------------------------------------------------------------------+
|                         PRESENTATION TIER (HTML)                              |
|  - Django templates + Bootstrap 5                                             |
|  - Responsive layouts and server-rendered forms                               |
|  - Custom CSS for portal styling                                               |
+-------------------------------------------------------------------------------+
                                       |
                                       | Django URL routing and template responses
                                       v
+-------------------------------------------------------------------------------+
|                         APPLICATION TIER                                      |
|  - Python and Django views/forms                                              |
|  - Role guards for seeker, recruiter, and administrator access                |
|  - Django ORM business logic and audit trail events                           |
|  - In-app notification dispatcher                                             |
+-------------------------------------------------------------------------------+
                                       |
                                       | Django ORM
                                       v
+-------------------------------------------------------------------------------+
|                           PERSISTENCE DATABASE TIER                           |
|  - SQLite 3 Relational Database Engine (db.sqlite3)                           |
|  - Django migrations and model constraints                                    |
|  - Enforced foreign key relationships                                         |
|  - Normalized relational tables                                                |
+-------------------------------------------------------------------------------+
```

---

## 2. Request-Response Lifecycle: Application Status Update Workflow

When a recruiter advances an applicant's stage:

1. **Form Action:** Recruiter selects a new stage and submits interview details and remarks through a Django form.
2. **View Verification:** Django checks the caller's authentication identity and verifies ownership of the job vacancy.
3. **Database Transaction:**
   - `job_applications.current_status` is updated.
   - A new row is inserted into `application_status_history` logging `previous_status`, `new_status`, `changed_by_user_id`, and `remarks`.
   - If `Interview Scheduled`, a corresponding record is written into the `interviews` table.
   - A new row is inserted into `notifications` targeting the job seeker.
4. **Response:** Django redirects to the recruiter view with a success message. The candidate sees the updated tracker and notification on the next page request.

---

## 3. Data Protection & Tenant Isolation

- **Recruiter Scoping:** SQL queries for applicants explicitly join `jobs` and check `WHERE jobs.recruiter_id = ?`. Even if an adversarial recruiter guesses another application ID, the query returns 404/403.
- **Candidate Privacy:** Candidates can only view applications where `job_applications.seeker_id = ?`.
- **Admin Privilege:** Administrative endpoints are guarded by strict role verification (`user.role === 'admin'`).
