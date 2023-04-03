# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Set the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy the package directory
COPY interview_orbital_materials ./interview_orbital_materials

# Stage 2: Runtime
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the package directory and run.py script from the builder stage
COPY --from=builder /app/interview_orbital_materials ./interview_orbital_materials
COPY --from=builder /app/run.py ./

# Set the entrypoint
ENTRYPOINT ["python", "run.py"]
