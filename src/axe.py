import os
import json
import subprocess
import pika
import time
import threading
from flask import Flask, jsonify, request, Response
from utils.auth import catch_rabbits
from utils.watch import logger
from utils.process import axe_scan
from prometheus_client import Counter, Histogram, generate_latest
from concurrent.futures import ThreadPoolExecutor, TimeoutError

app = Flask(__name__)

@app.route('/')
def handle_request():
    return jsonify({'message': 'Welcome to the Axe Scanner service!'})


def consume_urls():
    queue_name = 'axes_for_throwing'
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

            catch_rabbits(queue_name, callback)
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

    # Start consume_urls in a separate thread
    consume_thread = threading.Thread(target=consume_urls, daemon=True)
    consume_thread.start()

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=app_port)