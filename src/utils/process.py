import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
from utils.watch import logger
from flask import jsonify
from utils.yeet_back import axe_catcher
from utils.auth import rabbit
from selenium.common.exceptions import JavascriptException


def axe_scan(app, body, channel=None, delivery_tag=None):
    """
    Description:
        This function performs an accessibility audit using Axe-Core for a given URL.

    Args:
        app: The Flask application context.
        body: The HTTP POST request body containing the URL to be audited.
        channel: The RabbitMQ channel for the message. Default is None.
        delivery_tag: The RabbitMQ message delivery tag. Default is None.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the accessibility audit.
    """
    with app.app_context():
        url = None
        url_id = None
        try:
            if isinstance(body, str):  # Check if 'body' is a string
                payload = json.loads(body)
            else:
                payload = json.loads(body)
            url = payload.get('url')
            url_id = payload.get('url_id')
            logger.debug(f'🌟 Starting to process: {payload}')

            # Set the proxy settings using environment variables
            use_proxy = os.environ.get('USE_PROXY', 'false').lower() == 'true'
            proxy_http = os.environ.get('PROXY_HTTP')
            proxy_https = os.environ.get('PROXY_HTTPS')
            options = webdriver.ChromeOptions()
            if use_proxy:
                if proxy_http:
                    options.add_argument(f'--proxy-server={proxy_http}')
                if proxy_https:
                    options.add_argument(f'--proxy-server={proxy_https}')
            options.add_argument('--headless')
            options.add_argument('--single-process')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--stdout')
            options.add_argument('--remote-debugging-port=9222')
            options.binary_location = '/opt/google/chrome/chrome'

            # Disable file downloads
            prefs = {"download_restrictions": 3}  # Disable all downloads
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=options)

            logger.debug(f'Testing URL: {url}')
            driver.get(url)

            axe = Axe(driver)
            try:
                axe.inject()
            except JavascriptException as e:
                logger.error(f"Error injecting axe on {url}: {str(e)}")
                # Handle the exception or perform the desired actions
            else:
                results = axe.run()
                # Process the results as you wish

            # Debug Results
            results = axe.run()

            # Convert the results dictionary to a JSON string
            results_json = json.dumps(results)

            # Convert the JSON string back to a dictionary
            results_dict = json.loads(results_json)

            # Get Axe Driver Info
            user_agent = driver.execute_script("return navigator.userAgent;")
            window_width = driver.execute_script("return window.innerWidth;")
            window_height = driver.execute_script("return window.innerHeight;")
            orientation_angle = driver.execute_script("return window.orientation;")
            orientation_type = driver.execute_script("return screen.orientation && screen.orientation.type;")

            axe_driver_specs = {
                'engine_name': 'Axe',
                'orientation_angle': orientation_angle,
                'orientation_type': orientation_type,
                'user_agent': user_agent,
                'window_height': window_height,
                'window_width': window_width,
            }
            # logger.debug(f'Axe Driver Specs: {axe_driver_specs}')
            # Axe Shut Down
            driver.quit()

            # Yeet to Yeet Back
            axe_catcher(results_dict, url_id, axe_driver_specs)

            if channel and delivery_tag:
                channel.basic_ack(delivery_tag)

        except Exception as e:
            logger.error(f'❌ Error processing URL {url}: {e}', exc_info=True)

            # Send the URL to the axe_scan_error queue
            if url and url_id:
                # Send a message to the error_crawler queue
                error_payload = json.dumps({
                    "url_id": url_id,
                    "url": url,
                    "error_message": str(e)
                })
                rabbit('error_axe', error_payload)

            if channel and delivery_tag:
                channel.basic_nack(delivery_tag)
