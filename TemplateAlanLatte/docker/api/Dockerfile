# Stage 1: Building dependencies with poetry
FROM python:3.11-slim

# Install system-level dependencies including curl and git for fetching packages
#RUN apt-get update && \
#    apt-get install -y build-essential libpq-dev curl git

# Set working directory in the container
WORKDIR /app

# Copy only pyproject.toml & poetry.lock first to avoid rebuilding when code changes
COPY pyproject.toml poetry.lock ./

# Install dependencies using poetry
#RUN poetry config virtualenvs.create false && \
#    poetry install --no-root  
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Stage 2: Final lightweight runtime stage
#FROM python:3.11-slim

# Install basic utilities
#RUN apt-get update && \
#    apt-get install -y curl git

# Copy built dependencies from previous stage
#COPY --from=builder /root/.cache/pip /root/.cache/pip
#COPY --from=builder /usr/local/bin/* /usr/local/bin/
#COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages

# Create application directory and copy sources
#WORKDIR /app
COPY app ./app

# Expose port
EXPOSE 8000

# Command to start your application
CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
