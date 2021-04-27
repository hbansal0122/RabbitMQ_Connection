import unittest
import pika
from constants import HOST

class UnitTests(unittest.TestCase):

    def test_rabbitmq_channel(self):

        # Given
        message = "123"
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST))
        channel = connection.channel()
        channel.queue_declare(queue="test")

        # When
        channel.basic_publish(exchange='', routing_key="test", body=message)   

        # Then
        for _method_frame, _properties, body in channel.consume('test'):
            self.assertEqual(message, body.decode("utf-8"))
            channel.close()
            connection.close()

    
if __name__ == '__main__':
    unittest.main()