# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE exchange_center.settings
EXPOSE 8001

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nginx nano vim

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Add nginx user/group/config
RUN addgroup --system --gid 108 nginx && \
    adduser --system --disabled-password --ingroup nginx --no-create-home --gecos "nginx user" --shell /bin/false --uid 108 nginx

COPY nginx.conf /etc/nginx/nginx.conf

# Copy project files
COPY . /app/

# Set permissions
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/ && \
    chown -R nginx:nginx /var/lib/nginx && \
    chown -R nginx:nginx /usr/share/nginx

RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to nginx user
USER nginx

CMD ["sh", "-c", "nginx && gunicorn --bind 0.0.0.0:8001 exchange_center.wsgi:application"]

