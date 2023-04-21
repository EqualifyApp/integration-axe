import pika
from utils.watch import logger

def rabbit(queue_name):
    logger.debug('Connecting to RabbitMQ server...')
    credentials = pika.PlainCredentials('worker_axe', '$wFBN9Iu7vS7uf&')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.29', credentials=credentials, virtual_host='gova11y'))
    logger.debug('Connected to RabbitMQ server!')

    logger.debug(f'Declaring queue: {queue_name}...')
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True, arguments={'x-message-ttl': 7200000, 'x-max-length': 250, 'x-overflow': 'reject-publish'})
    logger.debug(f'Queue {queue_name} declared!')

    return channel, connection
