FROM python:3.11-alpine

# Install system dependencies including Tesseract OCR
# gcc, musl-dev, etc. are needed for compiling some Python packages
RUN apk add --no-cache \
    tesseract-ocr \
    tesseract-ocr-data-ind \
    tesseract-ocr-data-eng \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
# Force Rebuild: 2025-12-23-morning
COPY . .

# Create a non-root user for security
RUN adduser -D appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
