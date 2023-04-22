import json
import time
import pika
from utils.watch import logger
from utils.auth import rabbit


def axe_catcher(cleaned_results, url_id, axe_driver_specs):
    # logger.debug(f'Yeet Caught {url_id} ! \n Axe Driver Specs: {axe_driver_specs}')
    # logger.debug(f'Caught Cleaned Results: {cleaned_results}')

    tables_scans = {
            'engine_name': axe_driver_specs.get('engine_name'),
            'orientation_angle': axe_driver_specs.get('orientation_angle'),
            'orientation_type': axe_driver_specs.get('orientation_type'),
            'user_agent': axe_driver_specs.get('user_agent'),
            'window_height': axe_driver_specs.get('window_height'),
            'window_width': axe_driver_specs.get('window_width'),
            'scanned_at': cleaned_results.get('timestamp'),
            'url_id': url_id,
            'url': cleaned_results.get('url')
            }

    # Process the results and create tables_rules and tables_nodes lists
    tables_rules_list = []
    tables_nodes_list = []

    rule_types = ['violations', 'incomplete', 'inapplicable', 'passes']

    for rule_type in rule_types:
        for rule in cleaned_results.get(rule_type, []):
            tables_rules_item = {
                'rule_type': rule_type,
                'axe_id': rule.get('id'),
                'impact': rule.get('impact'),
                'tags': ','.join(rule.get('tags', []))
            }
            tables_rules_list.append(tables_rules_item)

            for node in rule.get('nodes', []):
                tables_nodes_item = {
                    'rule_id': '42',  # This should be replaced by the actual rule_id from the rules table
                    'failure_summary': node.get('failureSummary'),
                    'html': node.get('html'),
                    'impact': node.get('impact'),
                    'target': ','.join(t for target_list in node.get('target', []) for t in target_list),
                    'criteria_all': json.dumps(node.get('all', [])),
                    'criteria_any': json.dumps(node.get('any', [])),
                    'criteria_none': json.dumps(node.get('none', []))
                }
                tables_nodes_list.append(tables_nodes_item)

    # Prepare data for RabbitMQ
    data = {
        'tables_scans': tables_scans,
        'tables_rules': tables_rules_list,
        'tables_nodes': tables_nodes_list
    }
    message = json.dumps(data)

    # Send the data to the RabbitMQ queue

# This queue is for the table data
    queue_name = 'sharp_axes'
    channel, connection = rabbit(queue_name, message)
    if channel and connection:
        logger.info(f'🏆 Message sent to {queue_name}!')
    else:
        logger.error(f'Sick Rabbit! Sick Rabbit! Sick Rabbit! {queue_name}')

    # Send a confirmation message to the axe_speed queue
    # This queue is to track speed
    queue_name = 'axe_speed'
    body='VICTORY'
    channel, connection = rabbit(queue_name, body)
    if channel and connection:
        logger.info(f'🏆 Message sent to {queue_name}!')
    else:
        logger.error(f'Sick Rabbit! Sick Rabbit! Sick Rabbit! {queue_name}')
