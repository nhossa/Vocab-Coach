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

## 🌩️ AWS Deployment (Planned)

This application is designed for production deployment on AWS Free Tier:

### Infrastructure Components
- **ECS (Elastic Container Service)** - Container orchestration on t2.micro EC2
- **RDS PostgreSQL** - Managed database (t2.micro)
- **S3** - Database backup storage
- **Application Load Balancer** - Traffic distribution and SSL termination
- **CloudWatch** - Logging and monitoring
- **VPC** - Network isolation with public/private subnets
- **IAM** - Least-privilege roles for services
- **Security Groups** - Firewall rules

### Deployment Steps (Coming Soon)
1. Create RDS PostgreSQL instance
2. Create S3 bucket for backups
3. Build and push Docker image to ECR
4. Create ECS cluster and task definition
5. Deploy via GitHub Actions
6. Configure ALB with health checks
7. Update frontend config.js with production API URL

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
