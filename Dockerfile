# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Set PYTHONPATH so Python can find the 'app' package
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files first (for caching)
COPY poetry.lock pyproject.toml /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the full project including the database
COPY . .

# This line ensures your existing tasks.db is included
COPY tasks.db /app/tasks.db

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]