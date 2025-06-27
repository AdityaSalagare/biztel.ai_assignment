# --- Build Stage ---
# Use a full Python image to build dependencies that might have system requirements
FROM python:3.11 as builder

WORKDIR /app

# Install build dependencies if any
# RUN apt-get update && apt-get install -y build-essential

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies into the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
# Use a slim Python image for the final, smaller image
FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Download NLTK data
# This is done in the final stage to ensure data is in the image
RUN python -m nltk.downloader stopwords punkt wordnet

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the API server with Datadog tracing
# Set environment variables for API_KEY, BUGSNAG_API_KEY, DD_* in your runtime
CMD ["dd-trace-run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 