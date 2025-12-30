#  StackTutor — AI-Powered Technical Learning Platform

> A production-ready full-stack application demonstrating modern DevOps practices, cloud architecture, and AI integration.

**Live Demo:** *[Coming Soon - AWS Deployment]*

StackTutor is a cloud-native microservice that helps engineers master technical vocabulary across DevOps, Cloud, Backend, Networking, System Design, and Security. Built as a portfolio project showcasing real-world production patterns and AWS cloud infrastructure.

##  Project Highlights

- **Full-Stack Application**: FastAPI backend + responsive vanilla JavaScript frontend
- **AI Integration**: Google Gemini API for intelligent answer grading and term validation  
- **Production-Ready**: Docker containerization, environment-based configuration, structured logging
- **Cloud Architecture**: Designed for AWS deployment (ECS, RDS, S3, CloudWatch)
- **Security**: JWT authentication, rate limiting, input validation
- **Database**: PostgreSQL with SQLAlchemy ORM, 322+ pre-seeded technical terms
- **DevOps**: Infrastructure as Code ready, boto3 AWS integration, CI/CD prepared

---

##  Key Features

### AI-Powered Learning
- **Smart Grading**: Google Gemini evaluates user explanations with detailed feedback (scores, strengths, weaknesses)
- **Term Validation**: AI validates user-submitted terms for duplicates and categorizes them automatically
- **Intelligent Suggestions**: Users can suggest new terms with AI-powered approval workflow

###  Interactive Quizzes
- Category-based quiz selection (DevOps, Cloud, Backend, Networking, System Design, Security)
- Free-form answer submission with instant AI feedback
- Personal vocabulary tracking with review system
- Wrong answers automatically saved for targeted review

###  Secure Authentication
- JWT-based authentication with 30-minute token expiration
- User registration and login with bcrypt password hashing
- Protected API endpoints with bearer token authorization
- Rate limiting on sensitive endpoints (5/min login, 1/min quiz, 1/min suggestions)

### 💾 Robust Data Management
- PostgreSQL database with 322+ pre-seeded technical terms
- Browse all terms by category with filtering
- Personal vocabulary lists per user
- Automatic database backup to AWS S3 (production)

---

## Architecture

### Backend Stack
- **Framework**: FastAPI (async Python web framework)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Rate Limiting**: slowapi for endpoint protection
- **AI Service**: Google Gemini API for grading and validation
- **AWS Integration**: boto3 for S3 backup operations
- **Logging**: Structured JSON logging for CloudWatch integration

### Frontend Stack
- **HTML5 + CSS3** with Bootstrap 5.3.0
- **Vanilla JavaScript** with environment-aware API configuration
- **Responsive Design**: Mobile-friendly interface
- **Dynamic Routing**: Config-based API URL switching (dev/prod)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL with persistent volumes
- **Environment Management**: .env-based configuration
- **Cloud Provider**: AWS (ECS, RDS, S3, CloudWatch planned)
- **Deployment**: GitHub Actions CI/CD pipeline ready

---

##  Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- (Optional) AWS credentials for S3 backups

### Quick Start

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/nhossa/Vocab-Coach.git
   cd Vocab-Coach
   \`\`\`

2. **Set up environment variables**
   \`\`\`bash
   cp .env.example .env
   # Edit .env and add your credentials:
   # - GEMINI_API_KEY
   # - JWT_SECRET_KEY (generate with: openssl rand -hex 32)
   # - POSTGRES_USER and POSTGRES_PASSWORD
   \`\`\`

3. **Start the application**
   \`\`\`bash
   docker compose up -d --build
   \`\`\`

4. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

5. **Create an account**
   - Navigate to the Register page
   - Create your account
   - Start learning!

### Development Workflow

\`\`\`bash
# View logs
docker compose logs -f app

# Restart services
docker compose restart

# Stop services
docker compose down

# Rebuild after code changes
docker compose up -d --build

# Access database
docker compose exec db psql -U <your_user> -d vocab_coach
\`\`\`

---

##  Project Structure

\`\`\`
StackTutor/
├── app/
│   ├── routers/          # API endpoints (auth, quiz, terms, vocabulary)
│   ├── services/         # Business logic (AI client, S3 backup)
│   ├── auth/             # JWT authentication logic
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic request/response models
│   ├── database.py       # Database connection setup
│   ├── logging_config.py # Structured logging configuration
│   └── main.py           # FastAPI application entry point
├── frontend/
│   ├── *.html            # Frontend pages (login, quiz, dashboard, etc.)
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript (including config.js for env detection)
├── tests/                # Unit tests (pytest)
├── docker-compose.yml    # Multi-container setup
├── Dockerfile            # Application container
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── README.md             # This file
\`\`\`

---

##  Key Technologies

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation using Python type hints
- **PyJWT** - JSON Web Token implementation
- **passlib** - Password hashing library
- **slowapi** - Rate limiting for FastAPI
- **boto3** - AWS SDK for Python
- **python-json-logger** - Structured logging

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - Modern HTTP client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline (ready)
- **AWS Services** - ECS, RDS, S3, CloudWatch (deployment ready)

---

##  Security Features

- **Password Hashing**: bcrypt with salt rounds
- **JWT Tokens**: Secure bearer token authentication
- **Rate Limiting**: Protection against abuse (login, quiz, suggestions)
- **Input Validation**: Pydantic schemas for all API inputs
- **Environment Variables**: Secrets never hardcoded
- **CORS Configuration**: Environment-based access control
- **SQL Injection Protection**: SQLAlchemy ORM parameterization

---

##  API Endpoints

### Authentication
- \`POST /api/v1/auth/register\` - Create new user account
- \`POST /api/v1/auth/login\` - Login and receive JWT token

### Terms
- \`GET /api/v1/terms/{term_id}\` - Get specific term details
- \`GET /api/v1/terms/all\` - Browse all terms (with category filter)
- \`POST /api/v1/terms/suggest\` - Suggest new term (AI validated, rate limited)

### Quiz
- \`GET /api/v1/quiz/random\` - Get random quiz question by category
- \`POST /api/v1/quiz/answer\` - Submit answer for AI grading (rate limited)

### Vocabulary
- \`GET /api/v1/vocabulary\` - Get user's vocabulary list
- \`POST /api/v1/vocabulary\` - Add term to vocabulary
- \`DELETE /api/v1/vocabulary/{item_id}\` - Remove from vocabulary

All protected endpoints require \`Authorization: Bearer <token>\` header.

---

## 🌩️ AWS Deployment

This application is production-ready for AWS deployment. Here's the complete setup guide.

### Prerequisites
- AWS Account with Free Tier eligible t2.micro instances
- AWS CLI configured with credentials
- Docker and Docker Compose installed locally
- GitHub repository set up for CI/CD

### Step-by-Step AWS Deployment

#### 1. Create RDS PostgreSQL Database
```bash
# Via AWS Console:
# 1. Go to RDS → Create database
# 2. Choose PostgreSQL 15
# 3. Templates: Free tier
# 4. Instance identifier: stacktutor-db
# 5. Master username: vocabuser
# 6. Auto-generate password (save to Secrets Manager)
# 7. Connectivity: Public accessibility = Yes (for initial setup)
# 8. Create database
```

#### 2. Create S3 Bucket for Backups
```bash
# Via AWS Console or CLI:
aws s3 mb s3://stacktutor-backups-$(date +%s) --region us-east-1

# Enable versioning for backup recovery
aws s3api put-bucket-versioning \
  --bucket stacktutor-backups-xxxxx \
  --versioning-configuration Status=Enabled
```

#### 3. Create ECR Repository
```bash
# Push Docker image to Elastic Container Registry
aws ecr create-repository --repository-name stacktutor --region us-east-1

# Get login token and push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t stacktutor .
docker tag stacktutor:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/stacktutor:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/stacktutor:latest
```

#### 4. Create ECS Cluster
```bash
# Via AWS Console:
# 1. ECS → Clusters → Create cluster
# 2. Name: stacktutor-cluster
# 3. Infrastructure: EC2 (t2.micro)
# 4. Create
```

#### 5. Create ECS Task Definition
```bash
# Via AWS Console:
# 1. ECS → Task definitions → Create new task definition
# 2. Family: stacktutor-task
# 3. Container name: stacktutor
# 4. Image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/stacktutor:latest
# 5. Port mappings: 8001 → 8001
# 6. Environment variables:
#    - ENVIRONMENT=production
#    - DATABASE_URL=postgresql://vocabuser:password@rds-endpoint:5432/vocabdb
#    - GEMINI_API_KEY=<your-api-key>
#    - SECRET_KEY=<your-secret>
#    - AWS_REGION=us-east-1
# 7. Create
```

#### 6. Create Application Load Balancer
```bash
# Via AWS Console:
# 1. EC2 → Load Balancers → Create ALB
# 2. Name: stacktutor-alb
# 3. Scheme: Internet-facing
# 4. Listeners: HTTP:80 → Target group
# 5. Create target group:
#    - Name: stacktutor-targets
#    - Protocol: HTTP
#    - Port: 8001
#    - Health check path: /ready
#    - Health check interval: 30 seconds
# 6. Create
```

#### 7. Create ECS Service
```bash
# Via AWS Console:
# 1. ECS → Clusters → stacktutor-cluster → Create service
# 2. Task definition: stacktutor-task
# 3. Service name: stacktutor-service
# 4. Desired count: 1 (scale up later)
# 5. Load balancing: ALB
# 6. Target group: stacktutor-targets
# 7. Health check grace period: 60 seconds
# 8. Create service
```

#### 8. Run Initial Migrations
```bash
# Connect to RDS instance and run migrations:
alembic upgrade head

# Or via Docker:
docker compose exec app alembic upgrade head
```

#### 9. Test Health Endpoints
```bash
# Get ALB DNS name from AWS Console
curl http://<alb-dns-name>/health    # Should return 200
curl http://<alb-dns-name>/alive     # Should return 200
curl http://<alb-dns-name>/ready     # Should return 200
```

---

## 📊 Monitoring & Logging

### CloudWatch Logs
Your application logs are automatically captured in CloudWatch:

```bash
# View logs via AWS CLI:
aws logs tail /aws/ecs/stacktutor-cluster --follow

# Logs appear in CloudWatch Console:
# CloudWatch → Log groups → /ecs/stacktutor-task
```

### JSON Log Format (Production)
All logs are structured JSON in production for easy querying:

```json
{
  "timestamp": "2025-12-30 10:15:42,123",
  "level": "INFO",
  "logger": "app.main",
  "message": "Application starting"
}
```

### Health Check Monitoring
Three endpoints for orchestration:
- `/health` - General app health (Docker healthcheck)
- `/alive` - Container is running (Kubernetes liveness probe)
- `/ready` - Ready to handle traffic (ECS/K8s readiness probe)

### CloudWatch Metrics & Alarms (ALB/ECS)
Recommended basic alarms (no app code changes needed):

```bash
# 1) ALB 5XX alarm (triggers on any 5xx over 5 minutes)
aws cloudwatch put-metric-alarm \
   --alarm-name stacktutor-alb-5xx \
   --namespace AWS/ApplicationELB \
   --metric-name HTTPCode_ELB_5XX_Count \
   --dimensions Name=LoadBalancer,Value=<alb-arn-suffix> \
   --statistic Sum --period 60 --evaluation-periods 5 --threshold 1 \
   --comparison-operator GreaterThanOrEqualToThreshold \
   --treat-missing-data notBreaching \
   --alarm-actions <sns-topic-arn>

# 2) ALB latency (p95 > 2s for 5 minutes)
aws cloudwatch put-metric-alarm \
   --alarm-name stacktutor-alb-latency-p95 \
   --namespace AWS/ApplicationELB \
   --metric-name TargetResponseTime \
   --dimensions Name=LoadBalancer,Value=<alb-arn-suffix> \
   --statistic p95 --period 60 --evaluation-periods 5 --threshold 2 \
   --comparison-operator GreaterThanThreshold \
   --treat-missing-data notBreaching \
   --alarm-actions <sns-topic-arn>

# 3) ECS task CPU > 80% (5 minutes)
aws cloudwatch put-metric-alarm \
   --alarm-name stacktutor-ecs-cpu-high \
   --namespace AWS/ECS \
   --metric-name CPUUtilization \
   --dimensions Name=ClusterName,Value=stacktutor-cluster Name=ServiceName,Value=stacktutor-service \
   --statistic Average --period 60 --evaluation-periods 5 --threshold 80 \
   --comparison-operator GreaterThanThreshold \
   --treat-missing-data notBreaching \
   --alarm-actions <sns-topic-arn>
```

- Replace `<alb-arn-suffix>` with the value after `app/` in your ALB ARN (see Console → EC2 → Load Balancers).
- Replace `<sns-topic-arn>` with an SNS topic for alerts (email/SMS/Slack via webhook bridge).
- For dashboards: create a CloudWatch Dashboard with widgets for `HTTPCode_ELB_5XX_Count`, `TargetResponseTime`, `RequestCount`, and ECS `CPUUtilization`.

---

## 🔐 Database Backup & Restore

### Automated Backups
```bash
# Backup database to S3
python backup_restore.py backup

# This creates: stacktutor_db_20251230_101542.sql
```

### List Backups
```bash
python backup_restore.py list
```

### Restore from Backup
```bash
# Restore latest backup
python backup_restore.py restore

# Or specify a specific backup file
python backup_restore.py restore stacktutor_db_20251230_101542.sql
```

---

## 🚀 GitHub Actions CI/CD

Automated testing and Docker build on every push to `main`:

```yaml
Workflow:
1. Push to main branch
2. GitHub Actions triggers
3. Run pytest
4. Build Docker image (multi-stage)
5. Cache build layers for speed
6. Ready to push to ECR (optional)
```

To add ECR push:
```yaml
# Add to .github/workflows/ci.yml:
- name: Push to ECR
  run: |
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
    docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/stacktutor:${{ github.sha }}
```

---

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check if database is reachable
psql $DATABASE_URL -c "SELECT 1"

# If connection fails:
# 1. Verify RDS security group allows port 5432 from your IP
# 2. Check DATABASE_URL format: postgresql://user:pass@host:5432/dbname
# 3. Ensure credentials are correct
```

### Health Checks Failing
```bash
# Check readiness endpoint
curl -v http://localhost:8001/ready

# If returns 503:
# 1. Database may not be running
# 2. Migrations not applied
# 3. Missing environment variables
```

### Logs Not Appearing
```bash
# Check log level
echo $LOG_LEVEL  # Should be INFO or DEBUG in production

# Restart app with logging enabled
docker compose up app --build

# Check Docker stdout
docker compose logs -f app
```

### API Returning 401 Unauthorized
```bash
# JWT token expired (30 min default)
# Solution: Login again to get new token

# Check SECRET_KEY is set
echo $SECRET_KEY

# Regenerate if lost:
openssl rand -hex 32
```

### Rate Limiting Issues
```bash
# Default limits:
# - Login: 5 requests per minute
# - Quiz: 1 request per minute
# - Suggestions: 1 request per minute

# Wait 1 minute before retrying or check IP
# Rate limit errors return 429 Too Many Requests
```

### Database Backup Fails
```bash
# Ensure AWS credentials are set
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1

# Check S3 bucket exists
aws s3 ls s3://stacktutor-backups-xxxxx

# Manually backup with pg_dump
pg_dump $DATABASE_URL > backup.sql
```

---

## 📝 Running Migrations

### Create New Migration
```bash
# After modifying app/models.py:
alembic revision --autogenerate -m "Describe the change"

# Review generated file in alembic/versions/

# Apply migration
alembic upgrade head
```

### Rollback Migration
```bash
# Rollback one step
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

See `MIGRATIONS.md` for detailed migration guide.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run in Docker
docker compose exec app pytest -v
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/best_practices.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/)

---

##  Testing

\`\`\`bash
# Run tests
docker compose exec app pytest

# Run with coverage
docker compose exec app pytest --cov=app

# Run specific test file
docker compose exec app pytest tests/test_auth.py
\`\`\`

---

##  Environment Variables

See \`.env.example\` for all required and optional environment variables:

**Required:**
- \`GEMINI_API_KEY\` - Google Gemini API key
- \`JWT_SECRET_KEY\` - Secret for JWT signing
- \`POSTGRES_USER\` - Database username
- \`POSTGRES_PASSWORD\` - Database password
- \`DATABASE_URL\` - PostgreSQL connection string

**Optional (Production):**
- \`ENVIRONMENT\` - Set to \`production\` for prod mode
- \`AWS_ACCESS_KEY_ID\` - For S3 backups
- \`AWS_SECRET_ACCESS_KEY\` - For S3 backups
- \`AWS_REGION\` - AWS region (default: us-east-1)
- \`S3_BACKUP_BUCKET\` - S3 bucket name for backups

---

##  Contributing

This is a portfolio project, but feedback and suggestions are welcome! Feel free to open an issue or submit a pull request.

---

##  License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Naim Hossain**
- GitHub: [@nhossa](https://github.com/nhossa)
- Project: [StackTutor](https://github.com/nhossa/Vocab-Coach)

Built as a portfolio project demonstrating full-stack development, cloud architecture, and DevOps practices.

---

## 🎓 Learning Resources

This project covers concepts from:
- DevOps (Docker, CI/CD, Infrastructure as Code)
- Cloud Architecture (AWS services, scalability, monitoring)
- Backend Engineering (REST APIs, database design, authentication)
- System Design (microservices, caching, rate limiting)
- Security (JWT, password hashing, input validation)
- AI Integration (LLM APIs, prompt engineering)

Perfect for interview preparation and real-world learning! 🚀
