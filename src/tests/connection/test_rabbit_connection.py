import unittest
import pika
from utils.auth import rabbit


class TestRabbitConnection(unittest.TestCase):
    def test_rabbit_connection(self):
        try:
            channel, connection = rabbit('test_queue')
            self.assertIsInstance(channel, pika.channel.Channel)
            self.assertIsInstance(connection, pika.adapters.blocking_connection.BlockingConnection)
        except Exception as e:
            self.fail(f"Failed to establish a connection to RabbitMQ: {str(e)}")
        finally:
            if connection and not connection.is_closed:
                connection.close()


if __name__ == '__main__':
    unittest.main()
