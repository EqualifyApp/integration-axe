import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
from utils.watch import logger
from flask import jsonify
from flask import current_app


def axe_scan(body):
    with current_app.app_context():
        try:
            payload = json.loads(body)
            url = payload.get('url')
            logger.debug('🌟 Starting to process: {payload}')

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            axe = Axe(driver)
            axe.inject()
            results = axe.run()

            driver.quit()

            return streamline_response(results)
        except Exception as e:
            logger.error(f'❌ Error processing URL {url}: {e}', exc_info=True)
            return jsonify({'error': str(e)}), 500


def streamline_response(results):
    with current_app.app_context():
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