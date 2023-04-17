import os
import json
import subprocess
from flask import Flask, request, jsonify

with open('src/axe.json') as f:
    header_mapping = json.load(f)

app = Flask(__name__)


def process_response(response_dict, mapping):
    processed = {}
    for key, value in response_dict.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                combined_key = f"{key}.{inner_key}"
                new_key = mapping.get(combined_key)
                if new_key:
                    processed[new_key] = inner_value
                else:
                    processed[combined_key] = inner_value
        else:
            new_key = mapping.get(key)
            if new_key:
                processed[new_key] = value
            else:
                processed[key] = value
    return processed


@app.route('/axe')
def axe_scan():
    url = request.args.get('url')
    # Get the proxy from the environment variable
    proxy = os.environ.get('http_proxy')
    cmd = f'axe {url} --chromedriver-path /usr/local/bin/chromedriver --chrome-options="no-sandbox" --stdout'
    if proxy:
        # Prepend the proxy environment variables to the command
        cmd = f'http_proxy={proxy} https_proxy={proxy} ' + cmd
    output = subprocess.check_output(cmd, shell=True)
    response = json.loads(output.decode('utf-8'))

    # Check if the response is a list and get the first item
    if isinstance(response, list) and len(response) > 0:
        response = response[0]
    # with open('../maps/axe.json') as f:
    # Define header mapping
    with open('src/axe.json') as f:
        header_mapping = json.load(f)

    # Process response
    transformed_response = process_response(response, header_mapping)

    # Return transformed response
    return jsonify(transformed_response)


if __name__ == '__main__':
    # Get the port number from the environment variable or use 8083 as default
    app_port = int(os.environ.get('APP_PORT', 8083))
    app.run(debug=True, host='0.0.0.0', port=app_port)
