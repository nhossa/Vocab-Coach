# FastAPI Learning Notes

## 📚 Key Concepts

### 1. **FastAPI vs Django**
- **Django**: Full-featured web framework (ORM, admin, templating, auth built-in)
- **FastAPI**: Lightweight, focuses on APIs, built for speed and async operations
- **Key difference**: FastAPI uses async/await for non-blocking I/O operations

### 2. **Async I/O Basics**
- **Synchronous**: Code waits for each operation to complete (blocking)
- **Asynchronous**: Code continues while waiting for I/O (non-blocking)
- Use `async def` for endpoints that do I/O operations (database, API calls)
- Use `await` when calling async functions

```python
# Synchronous - blocks while waiting
def get_user():
    user = db.query(User).first()  # waits here
    return user

# Asynchronous - doesn't block
async def get_user():
    user = await db.query(User).first()  # continues other work while waiting
    return user
```

### 3. **Project Structure**
- **models.py**: SQLAlchemy ORM - defines database tables (what data looks like in DB)
- **schemas.py**: Pydantic - defines request/response format (API validation)
- **routers/**: Organize endpoints by feature (auth, vocabulary, etc.)
- **main.py**: Application entry point, registers routers
- **database.py**: Database connection and session management

### 4. **Type Annotations**
FastAPI uses Python type hints for validation and documentation:
```python
def create_word(word: str, difficulty: int) -> dict:
    return {"word": word, "difficulty": difficulty}
```

### 5. **Docker Concepts**
- **Container**: Isolated environment that runs your app with all dependencies
- **Image**: Blueprint/template for creating containers (built from Dockerfile)
- **Dockerfile**: Recipe for building an image (instructions for setup)
- **Volume**: Persistent storage that survives container restarts
- **Port mapping**: Connect container port to host port (`-p 8000:8000`)

```dockerfile
# Dockerfile structure
FROM python:3.11-slim          # Base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependency file
RUN pip install -r requirements.txt  # Install dependencies
COPY . .                       # Copy application code
EXPOSE 8000                    # Document port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]  # Run command
```

---

## 🎯 What We're Building

A vocabulary learning API with:
1. User registration and JWT authentication
2. CRUD operations for vocabulary words
3. Database relationships (Users → Vocabulary Items)
4. Input validation with Pydantic
5. Async database operations
6. **Dockerized deployment** with volume mounts and port exposure
7. **Docker Compose** for running app + database together
8. **CI/CD pipeline** with GitHub Actions

---

## 📝 Progress Tracker

### ✅ Completed
- [x] FastAPI basic setup
- [x] Database configuration (SQLAlchemy)
- [x] Initial Pydantic schemas

### 🔄 In Progress
- [ ] SQLAlchemy models with relationships
- [ ] CRUD operations
- [ ] JWT authentication

### 📋 Todo
- [ ] Dockerfile creation (with volumes, ports, multi-stage build)
- [ ] Docker Compose setup (app + PostgreSQL)
- [ ] Error handling & middleware
- [ ] Testing with pytest
- [ ] Frontend integration
- [ ] CI/CD with GitHub Actions + Docker
