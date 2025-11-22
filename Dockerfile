# ----- STAGE 1: Build dependencies -----
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system libs ONLY in builder since some packages require system level compilers
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install deps into a separate directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ----- STAGE 2: Final lightweight image -----
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy the app code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
