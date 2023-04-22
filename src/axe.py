import os
import json
import subprocess
import pika
import time
from flask import Flask, jsonify, request, Response
from utils.auth import catch_rabbits
from utils.watch import logger
from utils.process import axe_scan
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

@app.route('/')
def handle_request():
    return jsonify({'message': 'Welcome to the Axe Scanner service!'})


def consume_urls():
    queue_name = 'axes_for_throwing'
    while True:
        try:
            catch_rabbits(queue_name, lambda ch, method, properties, body: axe_scan(app, body.decode('utf-8'), ch, method.delivery_tag))
        except Exception as e:
            logger.error(f'Error in consume_urls: {e}')
            time.sleep(5)


@app.route('/health')
def health_check():
    return jsonify({'status': 'UP'}), 200


@app.route('/axe')
def handle_axe_request():
    url = request.args.get('url')
    logger.info(f'[HTTP request] Scanning URL: {url}')

    with LATENCY.time():
        response = axe_scan(app, url)  # Pass the 'app' instance

    REQUESTS.inc()
    logger.info(f'[HTTP response] {response}')
    return response

# Prometheus
# Define metrics
REQUESTS = Counter('requests_total', 'Total number of requests')
LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')


@app.route('/metrics')
def metrics():
    # Collect and return the metrics as a Prometheus-formatted response
    response = Response(generate_latest(), mimetype='text/plain')
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


if __name__ == '__main__':
    # Get the port number from the environment variable or use 8083 as default
    app_port = int(os.environ.get('APP_PORT', 8083))
    consume_urls()
    app.run(debug=True, host='0.0.0.0', port=app_port)
