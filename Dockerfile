# Use an official Python runtime as a parent image
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate

# Use a multi-stage build to add Nginx
FROM nginx:alpine as nginx

# Copy the static files from the previous stage
COPY --from=base /app/staticfiles /usr/share/nginx/html/static

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 8080

# Start Nginx and Gunicorn
CMD ["sh", "-c", "nginx && gunicorn --bind 0.0.0.0:8080 exchange_center.wsgi:application"]
