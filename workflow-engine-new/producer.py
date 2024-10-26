# docker run -it --rm --name rabbitmq -p 5672:5672 rabbitmq:3.8.1-management
# pip install pika
# send message
import pika
import json

# establish connection with broker
def send_messages(queue_name, message):
    print("sends")
    
    # Establish connection with broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    args = {
        'x-dead-letter-exchange': 'dead_letter_exchange',  # Link to the dead-letter exchange
        'x-dead-letter-routing-key': 'dead_letter_queue',    # Optionally, set a routing key
        'x-message-ttl': 60000  # Optional: TTL (in milliseconds) for messages in the main queue
    }
    
    channel.queue_declare(queue=queue_name, durable=True, arguments=args)
    # Declare the queue

    # Send the message
    channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode())
    
    print(message)

    # Close the connection
    connection.close()

# docker pull 8200artifactory.d8200.mil/docker-7170-remote-cache/430/eagle/rabbitmq:3.8.1-management
# docker run -it --rm --name rabbitmq -p 5672:5672 8200artifactory.d8200.mil/artifactory/docker-images-local/rabbitmq:3.8.1-management
