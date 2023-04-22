import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
from utils.watch import logger
from flask import jsonify
from utils.yeet_back import axe_catcher

def axe_scan(app, body, channel=None, delivery_tag=None):
    with app.app_context():
        try:
            if isinstance(body, str):  # Check if 'body' is a string
                payload = json.loads(body)
            else:
                payload = json.loads(body)
            url = payload.get('url')
            url_id = payload.get('url_id')
            logger.debug(f'🌟 Starting to process: {payload}')

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--stdout')

            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

            logger.debug(f'Testing URL: {url}')
            driver.get(url)

            axe = Axe(driver)
            axe.inject()

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
            return ({'error': str(e)}), 500


# Tests
def test_axe_scan():
    body = json.dumps({'url': 'https://example.com'})
    response = axe_scan(body)
    assert response.status_code == 200
    data = response.json
    assert 'url' in data
    assert 'results' in data
