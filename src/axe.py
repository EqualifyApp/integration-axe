import os
import json
import subprocess
import pika
import time
import threading
from functools import wraps
from flask import Flask, jsonify, request, Response
from utils.auth import catch_rabbits
from utils.watch import logger
from utils.process import axe_scan
from prometheus_client import Counter, Histogram, generate_latest
from concurrent.futures import ThreadPoolExecutor, TimeoutError

app = Flask(__name__)


@app.route('/')
def handle_request():
    """
    Description:
        Handles the root URL and returns a welcome message.

    Returns:
        A JSON object containing the welcome message.
    """
    return jsonify({'message': 'Welcome to the Axe Scanner service!'})


def consume_urls():
    """
    Description:
        Consumes URLs from a RabbitMQ queue and processes them using the axe_scan function.

    Raises:
        Any exceptions raised by the axe_scan function.
    """
    queue_name = 'launch_axe'
    while True:
        try:
            def callback(ch, method, properties, body):
                with ThreadPoolExecutor(max_workers=1) as executor:
                    try:
                        future = executor.submit(axe_scan, app, body.decode('utf-8'), ch, method.delivery_tag)
                        future.result(timeout=15)  # Set a timeout of 15 seconds
                    except TimeoutError:
                        logger.error(f'❌ Timeout reached while processing URL')
                        ch.basic_nack(method.delivery_tag)

            # Consume URLs from the RabbitMQ queue using the catch_rabbits function from utils/auth.py
            catch_rabbits(queue_name, callback)
        except Exception as e:
            # Log any errors that occur while consuming URLs from the queue
            logger.error(f'Error in consume_urls: {e}')
            # Wait 5 seconds before trying again
            time.sleep(5)


@app.route('/health')
def health_check():
    """
    Description:
        Returns the health status of the service.

    Returns:
        A JSON object containing the status 'UP'.
    """
    return jsonify({'status': 'UP'}), 200


@app.route('/axe')
def handle_axe_request():
    """
    Description:
        Handles requests to scan a URL with the Axe accessibility testing tool.

    Returns:
        The response from the axe_scan function.
    """
    # Get the URL to scan from the query string parameter 'url'
    url = request.args.get('url')
    # Log that a URL is being scanned
    logger.info(f'[HTTP request] Scanning URL: {url}')

    # Use the axe_scan function to scan the URL and pass the 'app' instance
    with LATENCY.time():
        response = axe_scan(app, url)

    # Increment the 'REQUESTS' counter for the Prometheus metrics
    REQUESTS.inc()
    # Log the response from the axe_scan function
    logger.info(f'[HTTP response] {response}')
    # Return the response from the axe_scan function
    return response


# Prometheus
# Define metrics
REQUESTS = Counter('requests_total', 'Total number of requests')
LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

def measure_latency(endpoint):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            start_time = time()
            response = func(*args, **kwargs)
            LATENCY.labels(endpoint=endpoint).observe(time() - start_time)
            REQUESTS.labels(endpoint=endpoint).inc()
            return response
        return wrapped
    return decorator

@app.route('/metrics')
def metrics():
    """
    Description:
        Returns the Prometheus metrics for the service.

    Returns:
        A Prometheus-formatted response containing the metrics.
    """
    # Collect and return the metrics as a Prometheus-formatted response
    response = Response(generate_latest(), mimetype='text/plain')
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


# Start the Flask app and consume URLs in a separate thread
if __name__ == '__main__':
    # Get the port number from the environment variable or use 8083 as default
    app_port = int(os.environ.get('APP_PORT', 8083))

    # Start consume_urls in a separate thread
    consume_thread = threading.Thread(target=consume_urls, daemon=True)
    consume_thread.start()

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=app_port)
