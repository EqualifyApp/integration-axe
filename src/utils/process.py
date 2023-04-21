import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
from utils.watch import logger
from flask import jsonify
from utils.yeet_back import axe_catcher


def axe_scan(app, body):
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

            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
            logger.debug(f'Testing URL: {url}')
            driver.get(url)

            axe = Axe(driver)
            axe.inject()
            results = axe.run()
    #    logger.debug(f'Raw axe results: {results}')

            driver.quit()

            streamlined_results = streamline_response(app, results)
            axe_catcher(streamlined_results, url_id)
        except Exception as e:
            logger.error(f'❌ Error processing URL {url}: {e}', exc_info=True)
            time.sleep(5)
            return jsonify({'error': str(e)}), 500


def streamline_response(app, results):
    with app.app_context():
        try:
            # Define the field mapping
            field_mapping = {
                'timestamp': 'scanned_at',
                'url': 'url',
                'testEngine.name': 'engine_name',
                'testEngine.version': 'engine_version',
                'testRunner.name': 'runner_name',
                'testEnvironment.userAgent': 'env_user_agent',
                'testEnvironment.windowWidth': 'env_window_width',
                'testEnvironment.windowHeight': 'env_window_height',
                'testEnvironment.orientationAngle': 'env_orientation_angle',
                'testEnvironment.orientationType': 'env_orientation_type',
                'toolOptions.reporter': 'reporter'
            }

            # Extract the fields we want to keep and rename them using the mapping
            streamlined_results = {}
            for original_field, new_field in field_mapping.items():
                if original_field in results:
                    streamlined_results[new_field] = results[original_field]

            # Remove unnecessary fields from inapplicable violations
            if 'inapplicable' in results:
                for result in results['inapplicable']:
                    trim_resulting_fat(result)

            # Remove unnecessary fields from incomplete violations
            if 'incomplete' in results:
                for result in results['incomplete']:
                    trim_resulting_fat(result)

            # Remove unnecessary fields from violations
            if 'violations' in results:
                for result in results['violations']:
                    trim_resulting_fat(result)

            # Remove unnecessary fields from passes
            if 'passes' in results:
                for pass_item in results['passes']:
                    del pass_item['description']
                    del pass_item['help']
                    del pass_item['helpUrl']
                    # Keep all other fields

            logger.debug('✅ Results have been streamlined')
            logger.debug(f'Streamlined results: {streamlined_results}')
            return jsonify(streamlined_results)
        except Exception as e:
            logger.error(f'❌ Error streamlining results: {e}', exc_info=True)
            return jsonify({'error': str(e)}), 500


def trim_resulting_fat(result):
    del result['description']
    del result['help']
    del result['helpUrl']
    # Keep all other fields


# Tests
def test_axe_scan():
    body = json.dumps({'url': 'https://example.com'})
    response = axe_scan(body)
    assert response.status_code == 200
    data = response.json
    assert 'url' in data
    assert 'results' in data