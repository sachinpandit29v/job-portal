import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

from accounts.models import User, JobSeekerProfile
from recruiters.models import Company, RecruiterProfile
from jobs.models import JobCategory, Job, SavedJob, JobReport
from applications.models import JobApplication, ApplicationStatusHistory, Interview
from notifications.models import Notification

def seed_database():
    print("Clearing previous seed data...")
    Notification.objects.all().delete()
    Interview.objects.all().delete()
    ApplicationStatusHistory.objects.all().delete()
    JobApplication.objects.all().delete()
    SavedJob.objects.all().delete()
    JobReport.objects.all().delete()
    Job.objects.all().delete()
    JobCategory.objects.all().delete()
    RecruiterProfile.objects.all().delete()
    Company.objects.all().delete()
    JobSeekerProfile.objects.all().delete()
    User.objects.all().delete()

    print("Seeding Administrators...")
    admin = User.objects.create_superuser(
        email='admin@jobportal.io',
        password='admin123',
        full_name='System Administrator',
        role='admin',
        phone='+1 (555) 019-2834'
    )

    print("Seeding Companies...")
    c1 = Company.objects.create(
        name='NexaTech Systems',
        slug='nexatech-systems',
        website='https://nexatech.example.com',
        location='San Francisco, CA (Hybrid / Remote)',
        industry='Enterprise Cloud & Distributed Systems',
        company_size='250-500 employees',
        description='NexaTech builds hyper-scale cloud data infrastructure, distributed workflows, and resilient real-time streaming platforms powering Fortune 500 enterprises.'
    )

    c2 = Company.objects.create(
        name='CloudWave AI',
        slug='cloudwave-ai',
        website='https://cloudwave.example.com',
        location='Austin, TX (Remote Friendly)',
        industry='Generative AI & MLOps Infrastructure',
        company_size='50-100 employees',
        description='CloudWave AI builds developer platforms and automated evaluation pipelines for enterprise Foundation Models, serving billions of inference queries daily.'
    )

    c3 = Company.objects.create(
        name='Veridian FinTech',
        slug='veridian-fintech',
        website='https://veridian.example.com',
        location='New York, NY (Hybrid)',
        industry='Algorithmic Trading & High-Frequency Ledgers',
        company_size='100-250 employees',
        description='Veridian designs ultra-low-latency order execution systems, automated market making microservices, and institutional crypto settlement engines.'
    )

    c4 = Company.objects.create(
        name='Loom Health',
        slug='loom-health',
        website='https://loomhealth.example.com',
        location='Boston, MA (Remote)',
        industry='Healthcare Technology & Clinical Intelligence',
        company_size='20-50 employees',
        description='Loom Health unifies clinical trial telemetry and EHR interoperability using privacy-preserving federated machine learning.'
    )

    print("Seeding Recruiters...")
    recruiter_user1 = User.objects.create_user(
        email='sarah.recruiter@nexatech.com',
        password='recruiter123',
        full_name='Sarah Jenkins',
        role='recruiter',
        phone='+1 (415) 890-1234'
    )
    RecruiterProfile.objects.create(
        user=recruiter_user1,
        company=c1,
        department='Technical Talent Acquisition',
        designation='Lead Technical Recruiter'
    )

    recruiter_user2 = User.objects.create_user(
        email='marcus.recruiter@cloudwave.io',
        password='recruiter123',
        full_name='Marcus Vance',
        role='recruiter',
        phone='+1 (512) 440-5678'
    )
    RecruiterProfile.objects.create(
        user=recruiter_user2,
        company=c2,
        department='Engineering Recruiting',
        designation='Head of Talent Acquisition'
    )

    print("Seeding Job Seekers...")
    seeker1 = User.objects.create_user(
        email='alex.dev@gmail.com',
        password='seeker123',
        full_name='Alex Rivera',
        role='seeker',
        phone='+1 (650) 321-9876'
    )
    JobSeekerProfile.objects.create(
        user=seeker1,
        headline='Senior Full Stack Software Engineer | Python, Django, React, Cloud Architecture',
        bio='Passionate software engineer with 6+ years designing scalable SaaS backends, RESTful APIs, and event-driven architectures. Proven track record reducing API latency by 45% and maintaining 99.99% system availability.',
        skills='Python, Django, PostgreSQL, Docker, Kubernetes, TypeScript, React, Redis, AWS, CI/CD',
        education='B.S. in Computer Science, University of California, Berkeley (2018)',
        experience_years=6,
        location='San Francisco, CA (Open to Remote)',
        github_url='https://github.com/alexrivera-dev',
        linkedin_url='https://linkedin.com/in/alexrivera-dev',
        portfolio_url='https://alexrivera.dev',
        resume_filename='Alex_Rivera_Senior_FullStack_Resume.pdf',
        resume_content="""# Alex Rivera
San Francisco, CA | alex.dev@gmail.com | (650) 321-9876 | linkedin.com/in/alexrivera-dev

## Professional Summary
Senior Software Engineer with 6+ years of experience architecting high-throughput distributed microservices in Python, Django, and Go. Passionate about clean code, automated testing, and developer experience.

## Technical Skills
- Languages: Python, JavaScript, TypeScript, SQL, Go, HTML5, CSS3
- Frameworks: Django, FastAPI, Express.js, React, Tailwind CSS, Bootstrap 5
- Databases: PostgreSQL, SQLite, Redis, DynamoDB
- Cloud & DevOps: AWS (ECS, Lambda, RDS), Docker, GitHub Actions, Terraform

## Professional Experience
### Lead Backend Engineer | FinScale Technologies (2021 - Present)
- Designed and delivered payment orchestration pipeline processing 25,000 requests/minute.
- Reduced database bottleneck latencies by 60% through query refactoring and Redis caching.
- Mentored 5 junior and mid-level engineers on automated CI/CD and clean architecture patterns.

### Full Stack Developer | MetroFlow Labs (2018 - 2021)
- Implemented real-time dashboard analytics using Django Channels and React.
- Maintained 95%+ unit and integration test coverage across core billing modules.

## Education
B.S. in Computer Science - University of California, Berkeley (2014 - 2018)"""
    )

    seeker2 = User.objects.create_user(
        email='priya.data@gmail.com',
        password='seeker123',
        full_name='Priya Sharma',
        role='seeker',
        phone='+1 (408) 555-7890'
    )
    JobSeekerProfile.objects.create(
        user=seeker2,
        headline='Machine Learning Scientist & Data Systems Engineer | PyTorch, NLP, MLOps',
        bio='Data Scientist specialized in Retrieval-Augmented Generation (RAG), vector indexing, and production ML model deployment. Published author at CVPR & NeurIPS workshops.',
        skills='Python, PyTorch, Scikit-learn, SQL, Spark, Pandas, Hugging Face, Ray, Docker, FastAPI',
        education='M.S. in Data Science, Stanford University (2021)',
        experience_years=4,
        location='San Jose, CA (Remote)',
        github_url='https://github.com/priyasharma-data',
        linkedin_url='https://linkedin.com/in/priyasharma-data',
        portfolio_url='https://priyasharma.io',
        resume_filename='Priya_Sharma_ML_Engineer_Resume.pdf',
        resume_content="""# Priya Sharma, M.S.
San Jose, CA | priya.data@gmail.com | (408) 555-7890

## Objective
Machine Learning Scientist with 4 years building enterprise LLM embeddings, recommendation systems, and scalable ML data pipelines.

## Education
- M.S. in Data Science, Stanford University (2019 - 2021)
- B.Tech in Computer Engineering, IIT Delhi (2015 - 2019)

## Skills
- Modeling: PyTorch, TensorFlow, Hugging Face Transformers, LangChain, Vector DBs (Pinecone, Chroma)
- Data Engineering: Apache Spark, SQL, Kafka, Pandas, NumPy
- Infrastructure: Docker, Kubernetes, AWS SageMaker, MLflow"""
    )

    seeker3 = User.objects.create_user(
        email='jordan.fresher@gmail.com',
        password='seeker123',
        full_name='Jordan Taylor',
        role='seeker',
        phone='+1 (617) 492-3344'
    )
    JobSeekerProfile.objects.create(
        user=seeker3,
        headline='Junior Software Engineer | 2026 CS Graduate | Python, Django, Web Dev',
        bio='Recent Computer Science graduate enthusiastic about full-stack web applications, clean REST APIs, and modern responsive frontends. Built multiple open-source full-stack projects.',
        skills='Python, Django, JavaScript, HTML5, CSS3, Bootstrap 5, SQLite, Git, Linux',
        education='B.S. in Computer Science, Boston University (Class of 2026)',
        experience_years=0,
        location='Boston, MA',
        github_url='https://github.com/jordantaylor-fresher',
        linkedin_url='https://linkedin.com/in/jordantaylor-cs',
        portfolio_url='https://jordantaylor.dev',
        resume_filename='Jordan_Taylor_Fresher_Portfolio_Resume.pdf',
        resume_content="""# Jordan Taylor
Boston, MA | jordan.fresher@gmail.com | github.com/jordantaylor-fresher

## Education
B.S. in Computer Science - Boston University (Graduation: May 2026)
GPA: 3.8 / 4.0 | Dean's Honor Roll

## Academic & Portfolio Projects
- Job Portal & Application Tracking System: Full-stack Django + SQLite web app with multi-role RBAC, visual ATS timeline, and resume uploads.
- Campus Event Booking: Python web app with scheduling notifications and role-based permissions.

## Technical Skills
- Core: Python, JavaScript, HTML5, CSS3, Bootstrap 5, SQL
- Tools: Git, VS Code, Linux Shell, Postman"""
    )

    print("Seeding Job Categories...")
    cats = {
        'fullstack': JobCategory.objects.create(name='Full Stack Engineering', slug='full-stack', description='End-to-end web and distributed service development.'),
        'frontend': JobCategory.objects.create(name='Frontend Engineering', slug='frontend', description='User interface, design systems, and client web applications.'),
        'backend': JobCategory.objects.create(name='Backend & Systems', slug='backend-systems', description='Distributed APIs, databases, microservices, and high-load servers.'),
        'ai_data': JobCategory.objects.create(name='Data Science & AI', slug='data-science-ai', description='Machine learning, analytics, LLM pipelines, and computer vision.'),
        'devops': JobCategory.objects.create(name='Cloud & DevOps', slug='cloud-devops', description='Kubernetes orchestration, CI/CD, cloud architecture, and SRE.'),
        'uiux': JobCategory.objects.create(name='UI/UX & Product Design', slug='ui-ux-design', description='User research, design tokens, responsive layouts, and user journeys.'),
        'mobile': JobCategory.objects.create(name='Mobile Engineering', slug='mobile-engineering', description='Native and cross-platform mobile apps for iOS and Android.'),
        'qa': JobCategory.objects.create(name='QA & Automation', slug='qa-automation', description='Test automation, integration pipelines, and system reliability testing.')
    }

    print("Seeding Job Vacancies...")
    # Job 1: Staff Full-Stack Architect @ NexaTech
    j1 = Job.objects.create(
        recruiter=recruiter_user1,
        company=c1,
        category=cats['fullstack'],
        title='Staff Full-Stack Architect',
        slug='staff-full-stack-architect',
        location='San Francisco, CA (Hybrid / Remote)',
        employment_type='Full-Time',
        experience_level='Senior',
        min_salary=160000,
        max_salary=210000,
        deadline=timezone.now().date() + timedelta(days=45),
        is_featured=True,
        views_count=142,
        status='active',
        description="""NexaTech Systems is seeking an experienced Staff Full-Stack Architect to lead the technical direction of our core enterprise cloud console. You will partner with principal engineers and product leaders to design next-generation developer portals, real-time workflow monitors, and mission-critical telemetry engines.

In this role, you will champion modern frontend and backend architectures, establish engineering best practices, and mentor a distributed team of 15+ software engineers across North America.""",
        responsibilities="""- Lead technical design and delivery of distributed cloud control planes handling millions of daily operations.
- Architect clean, reusable UI component libraries and high-throughput Python / Django backend APIs.
- Optimize database schemas, query plans, and distributed caching strategies for sub-50ms API responses.
- Drive engineering excellence: conduct rigorous code reviews, automated CI/CD pipeline improvements, and architecture RFC reviews.
- Mentor junior and mid-level engineers through paired programming and quarterly technical design workshops.""",
        requirements="""- 6+ years of professional full-stack software development experience with Python, TypeScript, and modern relational databases.
- Deep expertise in Django ORM, REST architectural patterns, and frontend state management.
- Demonstrated experience designing scalable systems deployed on AWS, GCP, or Azure with Docker and Kubernetes.
- Strong communication skills and ability to influence technical roadmaps across cross-functional engineering teams.
- Bachelor's or Master's degree in Computer Science or equivalent practical industry experience.""",
        benefits="""- Competitive salary with equity compensation package.
- Comprehensive health, dental, and vision insurance with 100% employer-covered premiums.
- $3,000 annual home office setup and continuous education learning stipend.
- Flexible PTO and 14 paid company holidays per calendar year."""
    )

    # Job 2: Senior Backend Systems Engineer @ CloudWave AI
    j2 = Job.objects.create(
        recruiter=recruiter_user2,
        company=c2,
        category=cats['backend'],
        title='Senior Backend Systems Engineer',
        slug='senior-backend-systems-engineer',
        location='Austin, TX (Remote Friendly)',
        employment_type='Full-Time',
        experience_level='Senior',
        min_salary=150000,
        max_salary=195000,
        deadline=timezone.now().date() + timedelta(days=30),
        is_featured=True,
        views_count=98,
        status='active',
        description="""CloudWave AI is scaling its inference gateway. We are looking for a Senior Backend Systems Engineer to build high-performance microservices, streaming event buses, and resilient model serving infrastructure.

You will work at the intersection of systems programming and AI pipelines, optimizing concurrency, throughput, and system reliability under heavy enterprise workloads.""",
        responsibilities="""- Build and maintain asynchronous REST and gRPC services capable of handling 50k+ requests/sec.
- Implement robust distributed rate limiting, queue management (RabbitMQ/Kafka), and Redis caching.
- Instrument telemetry, distributed tracing, and Prometheus metrics for real-time observability.
- Collaborate with ML engineers to streamline model checkpoint serialization and deployment pipelines.""",
        requirements="""- 5+ years building backend systems using Python (Django/FastAPI/AsyncIO) or Go.
- Solid understanding of distributed consensus, message brokers, and relational database internals.
- Proven experience deploying resilient Dockerized services in production environments.
- Passion for low-latency systems and clean architectural principles.""",
        benefits="""- Generous equity grants in a high-growth AI infrastructure startup.
- Full medical, dental, and vision coverage.
- Unlimited paid time off with mandatory 3-week minimum policy.
- Annual company retreat and sponsored conference attendance."""
    )

    # Job 3: Lead Machine Learning Scientist @ CloudWave AI
    j3 = Job.objects.create(
        recruiter=recruiter_user2,
        company=c2,
        category=cats['ai_data'],
        title='Lead Machine Learning Scientist',
        slug='lead-machine-learning-scientist',
        location='Austin, TX or Remote',
        employment_type='Full-Time',
        experience_level='Lead / Executive',
        min_salary=180000,
        max_salary=240000,
        deadline=timezone.now().date() + timedelta(days=60),
        is_featured=True,
        views_count=185,
        status='active',
        description="""Join CloudWave AI to lead research and engineering on our flagship LLM orchestration engine. We are solving open challenges in retrieval augmentation, context compression, and automated hallucination evaluation for Fortune 100 enterprise clients.""",
        responsibilities="""- Research, benchmark, and deploy cutting-edge foundation model fine-tuning and retrieval algorithms.
- Architect high-dimensional vector search pipelines and automated evaluation test suites.
- Author technical whitepapers and open-source benchmarks on generative AI reliability.
- Partner with product leaders to translate research breakthroughs into production features.""",
        requirements="""- M.S. or Ph.D. in Computer Science, Machine Learning, or related quantitative field.
- 4+ years applied experience with PyTorch, Hugging Face Transformers, and distributed training.
- Deep expertise in vector databases, embedding techniques, and prompt optimization frameworks.
- Strong publication or open-source track record in modern NLP / ML systems.""",
        benefits="""- Tier-1 equity package and performance bonuses.
- Top-tier workstation allowance (MacBook Pro + dual 4K monitors + GPU compute budget).
- Comprehensive health, mental wellness, and life insurance benefits."""
    )

    # Job 4: Junior Frontend Developer (Fresher / Entry-Level) @ NexaTech
    j4 = Job.objects.create(
        recruiter=recruiter_user1,
        company=c1,
        category=cats['frontend'],
        title='Junior Frontend Developer (Entry Level / 2026 Batch)',
        slug='junior-frontend-developer-entry-level',
        location='San Francisco, CA or Remote',
        employment_type='Full-Time',
        experience_level='Fresher / Entry',
        min_salary=75000,
        max_salary=95000,
        deadline=timezone.now().date() + timedelta(days=20),
        is_featured=False,
        views_count=230,
        status='active',
        description="""Looking to launch your career as a software engineer? NexaTech is hiring ambitious fresh graduates and early-career frontend developers to join our UI engineering team!

You will receive dedicated 1-on-1 mentorship from senior architects, contribute to live customer-facing portals, and master modern web standards including responsive layouts, accessibility (a11y), and performance optimization.""",
        responsibilities="""- Build responsive, accessible, and high-performance UI components using HTML5, CSS3, JavaScript, and Bootstrap.
- Collaborate with UX designers in Figma to translate wireframes into interactive web interfaces.
- Write unit and end-to-end tests to guarantee cross-browser compatibility.
- Participate in agile sprint planning, daily standups, and retrospective meetings.""",
        requirements="""- Bachelor's degree in Computer Science, Software Engineering, or related technical discipline (2025/2026 graduates encouraged!).
- Solid foundation in HTML, CSS, JavaScript, and modern DOM manipulation.
- Familiarity with CSS frameworks like Bootstrap 5 or Tailwind CSS.
- Understanding of Git version control workflows and RESTful APIs.
- Eagerness to learn, ask thoughtful questions, and grow rapidly as a software engineer.""",
        benefits="""- Structured 6-month graduate mentorship and engineering onboarding program.
- Competitive entry-level salary with annual review cycles.
- Full medical and dental coverage.
- $1,500 annual tech gear allowance."""
    )

    # Job 5: Principal Data Platform Engineer @ NexaTech
    j5 = Job.objects.create(
        recruiter=recruiter_user1,
        company=c1,
        category=cats['ai_data'],
        title='Principal Data Platform Engineer',
        slug='principal-data-platform-engineer',
        location='San Francisco, CA (Hybrid)',
        employment_type='Full-Time',
        experience_level='Senior',
        min_salary=175000,
        max_salary=225000,
        deadline=timezone.now().date() + timedelta(days=40),
        is_featured=False,
        views_count=76,
        status='active',
        description="""Architect NexaTech's next-generation analytical lakehouse processing terabytes of real-time telemetry. You will evaluate streaming compute engines, build declarative data contracts, and optimize distributed query performance.""",
        responsibilities="""- Design real-time data pipelines leveraging Kafka, Apache Spark, and Snowflake/BigQuery.
- Implement data governance, automated data quality validation, and lineage tracking.
- Collaborate with ML engineers and executive stakeholders on business analytics platforms.""",
        requirements="""- 7+ years building enterprise data platforms and petabyte-scale ETL pipelines.
- Expert-level SQL and Python skills.
- Deep familiarity with distributed data modeling (star schema, Data Vault) and cloud data warehouses.""",
        benefits="""- Top-tier compensation package.
- 401(k) matching up to 6%.
- Health, wellness, and commuter benefits."""
    )

    # Job 6: Associate Software Engineer @ Veridian FinTech
    j6 = Job.objects.create(
        recruiter=recruiter_user1,
        company=c3,
        category=cats['backend'],
        title='Associate Software Engineer - 2026 Batch',
        slug='associate-software-engineer-2026-batch',
        location='New York, NY (Hybrid)',
        employment_type='Full-Time',
        experience_level='Fresher / Entry',
        min_salary=85000,
        max_salary=105000,
        deadline=timezone.now().date() + timedelta(days=25),
        is_featured=False,
        views_count=112,
        status='active',
        description="""Veridian FinTech is expanding its algorithmic settlement engineering team. We are actively hiring entry-level software developers graduating in 2026 who are passionate about high-reliability systems, financial algorithms, and database optimization.""",
        responsibilities="""- Develop backend trade reconciliation services and automated transaction auditing tools.
- Optimize SQL queries and indexing structures for high-volume ledger transactions.
- Participate in daily peer code reviews and architectural discussions.""",
        requirements="""- Degree in Computer Science, Mathematics, or Electrical Engineering.
- Strong problem-solving skills and knowledge of data structures & algorithms.
- Experience with Python, SQL, and Unix/Linux environments.""",
        benefits="""- Competitive Wall Street base salary plus annual performance bonus.
- Comprehensive relocation assistance for candidates moving to NYC.
- Catered lunches and commuter transit passes."""
    )

    # Job 7: Senior Cloud & DevOps Engineer @ CloudWave AI
    j7 = Job.objects.create(
        recruiter=recruiter_user2,
        company=c2,
        category=cats['devops'],
        title='Senior Cloud & DevOps Engineer',
        slug='senior-cloud-devops-engineer',
        location='Remote (US)',
        employment_type='Full-Time',
        experience_level='Mid-Level',
        min_salary=140000,
        max_salary=175000,
        deadline=timezone.now().date() + timedelta(days=35),
        is_featured=False,
        views_count=64,
        status='active',
        description="""Maintain 99.99% uptime across multi-region Kubernetes clusters powering our generative inference APIs. Build declarative Terraform configurations, automated canary deployments, and chaos engineering drills.""",
        responsibilities="""- Manage multi-cloud Kubernetes clusters across AWS and GCP using GitOps and ArgoCD.
- Build resilient Terraform and Helm configurations for microservices infrastructure.
- Lead incident post-mortems and automate self-healing infrastructure checks.""",
        requirements="""- 4+ years managing production Kubernetes, Docker, and Linux cloud environments.
- Strong proficiency with Terraform, GitHub Actions, and Prometheus/Grafana.
- Background in Python or Bash automation scripting.""",
        benefits="""- 100% remote work flexibility from anywhere in the United States.
- Comprehensive health and life insurance.
- Continuous learning stipend for AWS/CKA certifications."""
    )

    # Job 8: Lead Product Designer (UI/UX) @ Loom Health
    j8 = Job.objects.create(
        recruiter=recruiter_user2,
        company=c4,
        category=cats['uiux'],
        title='Lead Product Designer (UI/UX)',
        slug='lead-product-designer-ui-ux',
        location='Boston, MA (Remote)',
        employment_type='Full-Time',
        experience_level='Senior',
        min_salary=130000,
        max_salary=165000,
        deadline=timezone.now().date() + timedelta(days=50),
        is_featured=False,
        views_count=87,
        status='active',
        description="""Design intuitive, accessible clinical dashboards that empower doctors and research scientists to save lives. You will own the full design lifecycle from qualitative user interviews to interactive Figma prototypes and design token systems.""",
        responsibilities="""- Conduct user research sessions with clinicians, patients, and research coordinators.
- Create wireframes, user journeys, design systems, and high-fidelity prototypes in Figma.
- Partner closely with frontend engineers to ensure pixel-perfect accessibility and responsive implementation.""",
        requirements="""- 5+ years of digital product design experience with complex web applications.
- Strong portfolio demonstrating systems thinking, user empathy, and typography hierarchy.
- Deep familiarity with accessibility (WCAG 2.1 AA) guidelines.""",
        benefits="""- Mission-driven healthcare technology culture.
- Flexible work hours and remote setup stipend.
- Comprehensive health, vision, and mental health wellness benefits."""
    )

    print("Seeding Candidate Applications & Visual ATS Timelines...")
    # App 1: Alex Rivera -> NexaTech (Staff Full-Stack Architect) -> SHORTLISTED
    app1 = JobApplication.objects.create(
        job=j1,
        seeker=seeker1,
        resume_filename=seeker1.seeker_profile.resume_filename,
        resume_content=seeker1.seeker_profile.resume_content,
        cover_letter="""Dear Sarah and the NexaTech Engineering Team,

I am writing to express my strong enthusiasm for the Staff Full-Stack Architect role. Having spent the last 6 years leading full-stack and distributed architecture at FinScale and MetroFlow Labs, I have developed deep expertise building reliable Python/Django services paired with high-performance client dashboards.

At FinScale, I redesigned our transaction processing layer to support 25k requests/min while cutting database latency by 60%. I would be thrilled to bring this dedication to NexaTech's distributed cloud platforms.

Looking forward to discussing how my experience can accelerate your roadmap!

Warm regards,
Alex Rivera""",
        current_status='Shortlisted',
        recruiter_notes="Strong candidate with proven 6-year track record in Django and distributed systems. Code samples check out exceptionally well. Shortlisted for technical panel."
    )

    # Status history for App 1:
    ApplicationStatusHistory.objects.create(
        application=app1,
        previous_status='Applied',
        new_status='Applied',
        changed_by=seeker1,
        remarks='Application submitted by candidate via online portal.',
        created_at=timezone.now() - timedelta(days=5)
    )
    ApplicationStatusHistory.objects.create(
        application=app1,
        previous_status='Applied',
        new_status='Under Review',
        changed_by=recruiter_user1,
        remarks='Resume and GitHub code repositories reviewed by technical recruiter Sarah Jenkins.',
        created_at=timezone.now() - timedelta(days=3)
    )
    ApplicationStatusHistory.objects.create(
        application=app1,
        previous_status='Under Review',
        new_status='Shortlisted',
        changed_by=recruiter_user1,
        remarks='Candidate shortlisted for technical panel interview. Scheduling coordinator contacted.',
        created_at=timezone.now() - timedelta(days=1)
    )

    # App 2: Alex Rivera -> CloudWave AI (Senior Backend Systems Engineer) -> INTERVIEW SCHEDULED
    intv_time = timezone.now() + timedelta(days=2, hours=4)
    app2 = JobApplication.objects.create(
        job=j2,
        seeker=seeker1,
        resume_filename=seeker1.seeker_profile.resume_filename,
        resume_content=seeker1.seeker_profile.resume_content,
        cover_letter="""Dear Marcus,

I have been following CloudWave AI's work on foundation model inference gateways with great excitement. My background in high-throughput Python backends and distributed concurrency directly matches your requirements for the Senior Backend Systems Engineer position.

I look forward to discussing how I can help scale your streaming pipelines.""",
        current_status='Interview Scheduled',
        interview_date=intv_time,
        interview_link='https://meet.google.com/qwe-rtyu-iop',
        recruiter_notes="Candidate has direct concurrency and messaging experience. Interview scheduled with Marcus Vance and Engineering Director."
    )

    ApplicationStatusHistory.objects.create(
        application=app2,
        previous_status='Applied',
        new_status='Applied',
        changed_by=seeker1,
        remarks='Application submitted.',
        created_at=timezone.now() - timedelta(days=7)
    )
    ApplicationStatusHistory.objects.create(
        application=app2,
        previous_status='Applied',
        new_status='Under Review',
        changed_by=recruiter_user2,
        remarks='Initial recruiter profile review completed.',
        created_at=timezone.now() - timedelta(days=5)
    )
    ApplicationStatusHistory.objects.create(
        application=app2,
        previous_status='Under Review',
        new_status='Shortlisted',
        changed_by=recruiter_user2,
        remarks='Profile passed initial screen. Advanced to interview round.',
        created_at=timezone.now() - timedelta(days=3)
    )
    ApplicationStatusHistory.objects.create(
        application=app2,
        previous_status='Shortlisted',
        new_status='Interview Scheduled',
        changed_by=recruiter_user2,
        remarks='Technical discussion scheduled via Google Meet.',
        created_at=timezone.now() - timedelta(days=1)
    )

    Interview.objects.create(
        application=app2,
        recruiter=recruiter_user2,
        seeker=seeker1,
        scheduled_at=intv_time,
        meeting_link='https://meet.google.com/qwe-rtyu-iop',
        notes='Round 1: 45-minute System Design & Architecture Discussion with Head of Talent Marcus Vance.',
        status='Scheduled'
    )

    # App 3: Priya Sharma -> CloudWave AI (Lead Machine Learning Scientist) -> INTERVIEW COMPLETED
    app3 = JobApplication.objects.create(
        job=j3,
        seeker=seeker2,
        resume_filename=seeker2.seeker_profile.resume_filename,
        resume_content=seeker2.seeker_profile.resume_content,
        cover_letter="""Dear Hiring Team at CloudWave AI,

I am applying for the Lead Machine Learning Scientist role. With an M.S. from Stanford and 4 years researching vector retrieval and LLM evaluation benchmarks, my research focus directly aligns with CloudWave's vision.

Best regards,
Priya Sharma, M.S.""",
        current_status='Interview Completed',
        recruiter_notes="Priya demonstrated exceptional domain expertise in vector databases and RAG pipelines. Interview round completed with outstanding scores."
    )

    ApplicationStatusHistory.objects.create(application=app3, previous_status='Applied', new_status='Applied', changed_by=seeker2, remarks='Application submitted by candidate.', created_at=timezone.now() - timedelta(days=12))
    ApplicationStatusHistory.objects.create(application=app3, previous_status='Applied', new_status='Under Review', changed_by=recruiter_user2, remarks='Research papers reviewed.', created_at=timezone.now() - timedelta(days=10))
    ApplicationStatusHistory.objects.create(application=app3, previous_status='Under Review', new_status='Shortlisted', changed_by=recruiter_user2, remarks='Candidate shortlisted.', created_at=timezone.now() - timedelta(days=7))
    ApplicationStatusHistory.objects.create(application=app3, previous_status='Shortlisted', new_status='Interview Scheduled', changed_by=recruiter_user2, remarks='Technical interview confirmed.', created_at=timezone.now() - timedelta(days=4))
    ApplicationStatusHistory.objects.create(application=app3, previous_status='Interview Scheduled', new_status='Interview Completed', changed_by=recruiter_user2, remarks='Technical discussion successfully conducted with Chief AI Scientist.', created_at=timezone.now() - timedelta(days=1))

    # App 4: Priya Sharma -> NexaTech (Principal Data Platform Engineer) -> SELECTED / OFFER!
    app4 = JobApplication.objects.create(
        job=j5,
        seeker=seeker2,
        resume_filename=seeker2.seeker_profile.resume_filename,
        resume_content=seeker2.seeker_profile.resume_content,
        cover_letter="""Dear NexaTech Recruitment,

I am excited to apply for the Principal Data Platform Engineer position. My background in building petabyte-scale distributed data pipelines and automated data contracts will enable NexaTech to achieve superior analytical velocity.""",
        current_status='Selected',
        recruiter_notes="Outstanding technical performance across all evaluation loops. Formal offer letter generated and delivered."
    )

    ApplicationStatusHistory.objects.create(application=app4, previous_status='Applied', new_status='Applied', changed_by=seeker2, remarks='Application registered in system.', created_at=timezone.now() - timedelta(days=20))
    ApplicationStatusHistory.objects.create(application=app4, previous_status='Applied', new_status='Under Review', changed_by=recruiter_user1, remarks='Profile screened by data committee.', created_at=timezone.now() - timedelta(days=16))
    ApplicationStatusHistory.objects.create(application=app4, previous_status='Under Review', new_status='Shortlisted', changed_by=recruiter_user1, remarks='Advanced to technical rounds.', created_at=timezone.now() - timedelta(days=12))
    ApplicationStatusHistory.objects.create(application=app4, previous_status='Shortlisted', new_status='Interview Scheduled', changed_by=recruiter_user1, remarks='Panel interview scheduled.', created_at=timezone.now() - timedelta(days=8))
    ApplicationStatusHistory.objects.create(application=app4, previous_status='Interview Scheduled', new_status='Interview Completed', changed_by=recruiter_user1, remarks='Unanimous positive feedback from data engineering panel.', created_at=timezone.now() - timedelta(days=4))
    ApplicationStatusHistory.objects.create(application=app4, previous_status='Interview Completed', new_status='Selected', changed_by=recruiter_user1, remarks='Official employment offer extended to Priya Sharma. Congratulations!', created_at=timezone.now() - timedelta(days=1))

    # App 5: Jordan Taylor -> NexaTech (Junior Frontend Developer) -> UNDER REVIEW
    app5 = JobApplication.objects.create(
        job=j4,
        seeker=seeker3,
        resume_filename=seeker3.seeker_profile.resume_filename,
        resume_content=seeker3.seeker_profile.resume_content,
        cover_letter="""Dear Sarah Jenkins,

As a passionate 2026 Computer Science graduate, I am very excited about NexaTech's Junior Frontend Developer opportunity. During my coursework and open-source projects, I have developed strong skills in responsive layouts, clean HTML5/CSS3, and modern JavaScript.

I look forward to contributing to your web applications while learning from your experienced engineering leaders!

Sincerely,
Jordan Taylor""",
        current_status='Under Review'
    )
    ApplicationStatusHistory.objects.create(application=app5, previous_status='Applied', new_status='Applied', changed_by=seeker3, remarks='Application submitted by fresher candidate.', created_at=timezone.now() - timedelta(days=2))
    ApplicationStatusHistory.objects.create(application=app5, previous_status='Applied', new_status='Under Review', changed_by=recruiter_user1, remarks='Fresher portfolio and GitHub projects being reviewed.', created_at=timezone.now() - timedelta(hours=8))

    # App 6: Jordan Taylor -> Veridian (Associate Software Engineer - 2026 Batch) -> APPLIED
    app6 = JobApplication.objects.create(
        job=j6,
        seeker=seeker3,
        resume_filename=seeker3.seeker_profile.resume_filename,
        resume_content=seeker3.seeker_profile.resume_content,
        cover_letter="""Dear Hiring Manager at Veridian FinTech,

I am writing to apply for the Associate Software Engineer role for the 2026 Batch. I am very interested in distributed ledgers and database query optimization.

Thank you for your consideration!

Best,
Jordan Taylor""",
        current_status='Applied'
    )
    ApplicationStatusHistory.objects.create(application=app6, previous_status='Applied', new_status='Applied', changed_by=seeker3, remarks='Initial application submitted.', created_at=timezone.now() - timedelta(hours=4))

    print("Seeding In-App Notifications...")
    # Notifications for Alex
    Notification.objects.create(
        user=seeker1,
        title="Application Stage: Shortlisted",
        message="Great news! Your application for 'Staff Full-Stack Architect' at NexaTech Systems has been Shortlisted.",
        link=f"/applications/{app1.id}/tracking/",
        is_read=False
    )
    Notification.objects.create(
        user=seeker1,
        title="Interview Scheduled with CloudWave AI",
        message="An interview for 'Senior Backend Systems Engineer' has been confirmed for " + intv_time.strftime('%b %d, %Y at %I:%M %p') + ".",
        link=f"/applications/{app2.id}/tracking/",
        is_read=False
    )

    # Notifications for Priya
    Notification.objects.create(
        user=seeker2,
        title="Offer Extended: Selected!",
        message="Congratulations! NexaTech Systems has selected you for the Principal Data Platform Engineer position.",
        link=f"/applications/{app4.id}/tracking/",
        is_read=False
    )

    # Notifications for Recruiters
    Notification.objects.create(
        user=recruiter_user1,
        title="New Fresher Application Received",
        message="Jordan Taylor submitted an application for 'Junior Frontend Developer (Entry Level / 2026 Batch)'.",
        link=f"/applications/recruiter/{app5.id}/",
        is_read=False
    )

    print("Seeding Bookmarks (Saved Jobs)...")
    SavedJob.objects.create(user=seeker1, job=j3)
    SavedJob.objects.create(user=seeker1, job=j7)
    SavedJob.objects.create(user=seeker2, job=j1)
    SavedJob.objects.create(user=seeker3, job=j1)
    SavedJob.objects.create(user=seeker3, job=j2)

    print("Seeding Compliance Reports...")
    JobReport.objects.create(
        job=j7,
        reporter=seeker3,
        reason='Misleading Salary or Title',
        details='Salary range seems different from company career page listing.',
        status='pending'
    )

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
