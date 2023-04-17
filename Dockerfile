# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        unzip \
        curl \
        libglib2.0-0 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxfixes3 \
        libxi6 \
        libxrandr2 \
        libxrender1 \
        libxss1 \
        libxtst6 \
        libgtk-3-0 \
        libasound2 \
        libdbus-glib-1-2 \
        libnspr4 \
        libnss3-tools \
        libxcb1 \
        wget gnupg unzip \
        libxslt1.1 \
        xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Install node and npm
    RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
    RUN apt-get install -y nodejs


# Install Selenium and its dependencies
    RUN apt-get update && apt-get install -y libglib2.0-0 libnss3 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxtst6 libatspi2.0-0 libappindicator3-1 libsecret-1-0
    RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
    RUN apt-get update && apt-get install -y google-chrome-stable
    RUN wget https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && mv chromedriver /usr/local/bin/
    RUN chmod +x /usr/local/bin/chromedriver


# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY src /app/src

# Install axe-cli
RUN npm install -g @axe-core/cli

# Make port available to the world outside this container
# The port number is now set as an environment variable with a default value of 8083
ENV APP_PORT 8083

# Set up the proxy environment variables
ENV http_proxy http://gluetun:18888
ENV https_proxy http://gluetun:18888

EXPOSE $APP_PORT

# Define environment variable
ENV FLASK_APP axe.py

# Run axe.py when the container launches
CMD ["python", "src/axe.py"]