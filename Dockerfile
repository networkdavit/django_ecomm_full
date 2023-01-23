FROM python:3.9.6-slim-buster

# Copy requirements.txt to container
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy rest of the application code to container
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=ecommerce.settings

# Expose port
EXPOSE 8000

# Start the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
