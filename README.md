Tech Vocab AI Coach — Cloud-Native Learning Microservice

Tech Vocab AI Coach is a cloud-native FastAPI microservice that teaches DevOps, Cloud, Backend Engineering, Networking, System Design, and Cybersecurity concepts through:

AI-simplified definitions

AI-graded free-form explanations

Category-based quizzes

Correct model answers

Personal vocabulary tracking

Full AWS-backed architecture

It combines backend engineering, async Python, SQLAlchemy ORM, RDS PostgreSQL, JWT auth, Docker, GitHub Actions CI/CD, AWS ECS, S3, IAM, and CloudWatch into one cohesive production-level project.

This is a real microservice — scalable, secure, and built using the same patterns companies use.

Features
🔹 Technical Learning Engine

Explain any technical term (DevOps, SWE, Security, System Design, Networking)

AI-generated simplified definitions

Real-world engineering examples

“Why this matters in real jobs”

Save vocabulary to a user’s account

Track mastery via review counts and quiz scores

🔹 AI-Powered Quiz System

User selects a category (DevOps, Networking, SWE, Security, System Design)

Service pulls a random term from RDS PostgreSQL

User explains the concept in their own words

AI compares user explanation to “ideal answer”

Returns:

score (0–100)

strengths

weaknesses

correct answer

Automatically saves weak terms to their account

🔹 Backend Architecture

FastAPI async endpoints

SQLAlchemy ORM with relationship mappings

JWT authentication & user scoping

CRUD APIs for Users, Terms, Vocabulary, Quiz Attempts

Background tasks for analytics + CloudWatch logs

Redis caching of definitions + terms

Type annotations everywhere

🔹 Cloud & DevOps

Docker containerization

AWS ECS Fargate deployment

AWS RDS PostgreSQL database

AWS S3 for terms dataset

AWS IAM roles (least privilege)

AWS CloudWatch logs + metrics

AWS CloudTrail auditing

GitHub Actions CI/CD pipeline

Optional Terraform for infrastructure-as-code

Cloud Architecture
                      Client (Web or Mobile)
                                 |
                                 v
                     Application Load Balancer
                                 |
                                 v
                         ECS Fargate Service
                        (FastAPI Containers)
                                 |
        --------------------------------------------------------
        |                                                      |
        v                                                      v
   RDS PostgreSQL                                      S3 (Terms Dataset)
   - users                                              - terms.json
   - terms                                              - category data
   - quiz_attempts
   - user_vocabulary
                                 |
                                 v
                     Redis Cache (optional improvement)
                                 |
                                 v
                   CloudWatch Logs & Custom Metrics
                                 |
                                 v
                           CloudTrail Auditing


This is a full production-grade microservice.

Database Schema (RDS PostgreSQL)
users
field	type	notes
id	PK	user id
email	varchar	unique
password_hash	text	JWT auth
created_at	timestamp	
terms
field	type	notes
id	PK	
term	varchar	
category	varchar	devops / networking / security / swe / system design
formal_definition	text	
simple_definition	text	
created_at	timestamp	
user_vocabulary
field	type	notes
id	PK	
user_id	FK → users	
term_id	FK → terms	
saved_at	timestamp	
review_count	int	
last_score	int	
quiz_attempts
field	type	notes
id	PK	
user_id	FK	
term_id	FK	
user_answer	text	
score	int	
ai_feedback	text	
correct_answer	text	
attempted_at	timestamp	
API Endpoints
1. Explain a Term
POST /api/v1/explain
{
  "term": "Load Balancer"
}


Response:

{
  "term": "Load Balancer",
  "formal_definition": "...",
  "simple_definition": "...",
  "examples": [...],
  "why_it_matters": "...",
  "timestamp": "2025-11-19T02:00:00Z"
}

2. Get a Quiz Question
GET /api/v1/quiz/random?category=devops


Response:

{
  "term_id": 42,
  "term": "CI/CD",
  "question": "Explain what CI/CD means."
}

3. Submit an Answer
POST /api/v1/quiz/answer
{
  "term_id": 42,
  "user_answer": "It's when code is automatically tested and deployed."
}


Response:

{
  "score": 78,
  "feedback": "Good start... but missing details like staging environments, pipelines, and automated deployment triggers.",
  "correct_answer": "CI/CD is ...",
  "saved_to_vocabulary": true
}

4. User Vocabulary
GET /api/v1/vocabulary/{user_id}

5. Auth (JWT)

POST /auth/register

POST /auth/login

Project Structure
Tech-Vocab-Coach/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── cache.py
│   ├── routers/
│   │   ├── explain.py
│   │   ├── quiz.py
│   │   ├── vocabulary.py
│   │   └── auth.py
│   └── services/
│       ├── ai_service.py
│       ├── aws_service.py
│       ├── quiz_service.py
│       └── logging_service.py
│
├── infra/
│   └── terraform/
│
├── tests/
│   ├── test_auth.py
│   ├── test_quiz.py
│   ├── test_explain.py
│   └── test_vocabulary.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .github/workflows/deploy.yml
├── .env.example
└── README.md

Local Setup
git clone https://github.com/YOUR_USERNAME/Tech-Vocab-Coach.git
cd Tech-Vocab-Coach

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload


Swagger UI:

http://localhost:8000/docs

Docker
docker build -t tech-vocab-coach .
docker run -p 8000:8000 tech-vocab-coach

CI/CD — GitHub Actions

Pipeline includes:

Lint + test

Build Docker image

Push to Amazon ECR

Deploy to ECS Fargate

YAML file included in .github/workflows/deploy.yml.

Environment Variables
OPENAI_API_KEY=your_key
JWT_SECRET=your_secret

POSTGRES_URL=postgresql://user:pass@host:5432/dbname

AWS_REGION=us-east-1
S3_BUCKET=techvocab-terms
CLOUDWATCH_LOG_GROUP=tech-vocab-logs

REDIS_URL=redis://localhost:6379

Why This Project Matters

This project demonstrates mastery of:

Backend engineering

Async Python

Modern API frameworks (FastAPI)

SQLAlchemy ORM modelling

JWT auth

Docker

AWS ECS deployment

RDS PostgreSQL

IAM roles

CloudWatch logging

CI/CD pipelines

AI integration

Data modeling

Full microservice architecture

This is a top-tier portfolio project for DevOps, Backend, Cloud, or Security Engineering.