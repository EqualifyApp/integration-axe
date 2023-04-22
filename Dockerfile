# Use an official Python runtime as a parent image
FROM python:3.9-alpine


# Install system dependencies
RUN apk update && \
    apk add --no-cache \
        wget \
        unzip \
        libx11 \
        libxcb \
        libxcomposite \
        libxcursor \
        libxdamage \
        libxext \
        libxfixes \
        libxi \
        libxrandr \
        libxrender \
        libxscrnsaver \
        libxtst \
        ca-certificates \
        ttf-freefont \
        libappindicator \
        libasound \
        atk \
        at-spi2 \
        at-spi2-core \
        at-spi2-atk \
        cairo \
        cups-libs \
        dbus \
        gdk-pixbuf \
        gtk+3.0 \
        nspr \
        nss \
        pango \
        xkeyboard-config \
        xdg-utils && \
    apk add --no-cache --virtual .build-deps \
        g++ \
        gcc \
        glib-dev \
        libc-dev \
        libx11-dev \
        libxcomposite-dev \
        libxcursor-dev \
        libxdamage-dev \
        libxext-dev \
        libxfixes-dev \
        libxi-dev \
        libxrandr-dev \
        libxrender-dev \
        libxscrnsaver-dev \
        libxtst-dev \
        make \
        musl-dev \
        pkgconfig

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    apk add --no-cache --allow-untrusted google-chrome-stable_current_x86_64.rpm && \
    rm google-chrome-stable_current_x86_64.rpm

# Install Chromedriver
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.24/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

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

# Cleanup build dependencies
RUN apk del .build-deps
