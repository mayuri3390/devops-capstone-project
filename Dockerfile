FROM python:3.9-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY service/ ./service/

# Create a non-root user and set permissions
RUN useradd --uid 1000 theuser && chown -R theuser:theuser /app
USER theuser

# Expose service port
EXPOSE 8080

# Run the service using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service:app"]
