# Stage 1: Builder
FROM python:3.10-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the project files and package directory
COPY . .

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Install dependencies into the virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Stage 2: Runtime
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the package directory from the builder stage
COPY --from=builder /app/interview_orbital_materials ./interview_orbital_materials

# Set the entrypoint
ENTRYPOINT ["python", "interview_orbital_materials/run.py"]
