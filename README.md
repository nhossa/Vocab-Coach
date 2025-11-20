# Tech Vocab AI Coach — Cloud-Native Learning Microservice

Tech Vocab AI Coach is a FastAPI-based microservice designed to help engineers quickly understand and retain technical vocabulary across DevOps, Cloud, Backend Engineering, Networking, System Design, and Security.

The service blends:

AI-generated definitions

AI-graded free-form explanations

Category-driven quizzes

Personal vocabulary tracking

JWT authentication

SQL-backed persistence

Dockerized, cloud-ready deployment

The system is structured like a real-world production microservice: clean API boundaries, async processing, caching, background analytics, and infrastructure that can be deployed directly to AWS.

## Features
### Technical Learning Engine

Provide any technical term (DevOps, SWE, System Design, Network, Security).

Returns a clean definition + simplified explanation.

Includes real-world engineering examples.

Stores terms to a user’s vocabulary list for spaced review.

### AI-Powered Quizzing

Users pick a category.

Service selects a random term from PostgreSQL.

User explains the concept in their own words.

AI evaluates the explanation against the ideal answer:

Score (0–100)

Strengths

Weak points

Correct definition

Weak terms are automatically saved for later review.

## Backend Architecture

FastAPI async endpoints

SQLAlchemy ORM with relationships

RDS PostgreSQL

JWT authentication + user scoping

CRUD endpoints for users, terms, vocabulary, quiz attempts

Background tasks for analytics + CloudWatch metrics

Optional Redis caching layer

Clean separation of routers, services, and models

Cloud & DevOps Stack

Docker containerization

ECS Fargate deployment

RDS PostgreSQL

S3 for term datasets

IAM least-privilege roles

CloudWatch logs + metrics

CloudTrail auditing

GitHub Actions CI/CD pipeline

Optional Terraform modules

This project intentionally mirrors real microservices used in production environments.
