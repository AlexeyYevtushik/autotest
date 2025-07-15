# Use official Python image
FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y <your-system-deps>

# Copy requirements first for better cache
COPY requirements.txt ./

# Install Python dependencies (if any)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Install Playwright browsers (chromium,webkit,firefox)
RUN playwright install --with-deps chromium 

# Ensure logs directory and file exist and are owned by appuser
RUN mkdir -p /app/logs \
    && touch /app/logs/app.log \
    && chmod -R 777 /app/logs

# Debugging step: Print permissions of /app/logs and /app/logs/app.log
RUN ls -ld /app/logs && ls -l /app/logs/app.log

# Copy the rest of the code
COPY . .

# Fix permissions for .pytest_cache
RUN mkdir -p /app/.pytest_cache
RUN mkdir -p /app/reports && chmod -R 777 /app/reports
RUN mkdir -p /app/tests/tmp && chmod -R 777 /app/tests/tmp

# Default command to smoke and full_run tests (can be overridden)
CMD ["pytest","-m smoke or full_run", "--html=reports/report.html", "--self-contained-html"]

# Uncomment the following line to run only smoke tests
#CMD ["pytest","-m smoke", "--html=reports/report.html", "--self-contained-html"]
