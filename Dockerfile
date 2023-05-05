# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        unzip \
        curl \
        libglib2.0-0 \
        libnss3 \
        gnupg \
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


# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Install Chrome driver
RUN LATEST_RELEASE=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST_RELEASE/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver
# Copy the rest of the application code
COPY src /app/src

ENV APP_PORT 8083
ENV RABBIT_USERNAME worker_axe
ENV RABBIT_PASSWORD pass_the_worker_axe
ENV RABBIT_HOST rabbit
ENV RABBIT_VHOST gova11y

# Define a health check
HEALTHCHECK --interval=2m --timeout=5s \
    CMD curl -f http://localhost:8083/health || exit 1

# Set up the proxy environment variables
ENV USE_PROXY false

# ENV QUEUE_NAME axes_for_throwing

EXPOSE $APP_PORT

# Define environment variable
ENV FLASK_APP axe.py

# Run axe.py when the container launches
CMD ["python", "src/axe.py"]
