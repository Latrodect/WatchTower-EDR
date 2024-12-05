import pika
import json

class MonitoringProducer:
    def __init__(self, host='localhost', port=5672, queue_name='monitoring_queue'):
        """
        RabbitMQ Producer class.

        :param host: The address of the RabbitMQ server (default: localhost)
        :param port: The port of the RabbitMQ server (default: 5672)
        :param queue_name: The name of the queue to which messages will be sent
        """
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        """
        Connect to RabbitMQ and declare a queue.

        This method establishes a connection with the RabbitMQ server
        on the specified host and port and declares a durable queue.
        """
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)  
            print(f"Connection established on {self.host}:{self.port} and queue '{self.queue_name}' is ready.")
        except Exception as e:
            print(f"Connection error: {e}")

    def publish(self, data: dict):
        """
        Publish data to the queue.

        :param data: The data to send, in dictionary format
        :raises Exception: If the channel is not connected
        """
        if not self.channel:
            raise Exception("You must connect to RabbitMQ before sending data. Call 'connect()' first.")
        
        try:
            message = json.dumps(data)
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2  
                )
            )
            print(f"Data pushed to queue '{self.queue_name}': {message}")
        except Exception as e:
            print(f"Message sending error: {e}")

    def close(self):
        """
        Close the RabbitMQ connection.

        This method closes the connection to RabbitMQ if it is open.
        """
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed.")
