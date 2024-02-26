##### Base Stage #####
FROM python:3.12-slim-bookworm as base

# Set default path
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH /app

##### Builder Stage #####
FROM base as builder

# Install libpq and gcc
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
        libpq-dev \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set default workdir
WORKDIR /app

# Create virtualenv and install Python packages
RUN pip install --no-cache-dir pip setuptools -U && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.in-project true
COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml
RUN poetry install --only main

# Copy app files to workdir
COPY rinha_2024_q1 ./rinha_2024_q1

##### Final Stage #####
FROM base

# Install libpq
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
        libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy content from builder stage
COPY --from=builder /app /app

# Add rinha user and create directories
RUN useradd -m rinha

# Set permissions
RUN chown -R rinha:rinha /app

# Set workdir and user
WORKDIR /app
USER rinha

# Expose port
EXPOSE 8000

# Set cmd
CMD ["python", "rinha_2024_q1/main.py"]
