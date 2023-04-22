# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        unzip \
        libglib2.0-0 \
        libnss3 \
        libx11-6 \
        libx11-xcb1 \
        libxcb1 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxi6 \
        libxrandr2 \
        libxrender1 \
        libxss1 \
        libxtst6 \
        ca-certificates \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcairo2 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgdk-pixbuf2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxfixes3 \
        libxinerama1 \
        libxkbcommon0 \
        libxrandr2 \
        libxshmfence1 \
        xdg-utils && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY src /app/src

ENV APP_PORT 8083
ENV RABBIT_USERNAME worker_axe
ENV RABBIT_PASSWORD PASSWORD_HERE
ENV RABBIT_HOST 192.168.1.29
ENV RABBIT_VHOST gova11y

# Set up the proxy environment variables
ENV http_proxy http://gluetun:8888
ENV https_proxy http://gluetun:8888

ENV QUEUE_NAME urls_scan-axe-1

EXPOSE $APP_PORT

# Define environment variable
ENV FLASK_APP axe.py

# Run axe.py when the container launches
CMD ["python", "src/axe.py"]
