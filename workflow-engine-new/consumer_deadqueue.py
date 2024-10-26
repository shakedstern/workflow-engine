import json
import pika

def callback(ch, method, properties, body):
    try:
        # Decoding and printing the message from the dead-letter queue
        body = body.decode()
        print("[x] Received from DLQ: %r" % body)

        # Acknowledge the message after successfully processing it
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        # Log any errors that occur during message processing
        print(f"Error processing message from DLQ: {e}. Skipping message.")

def consume_dead_letter_queue():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the dead-letter queue (make it durable to ensure messages persist)
    channel.queue_declare(queue="dead_letter_queue", durable=True)

    # Set up a consumer to listen to the dead-letter queue
    channel.basic_consume(queue="dead_letter_queue", on_message_callback=callback)

    print("Waiting for messages from the dead-letter queue...")
    # Start consuming messages from the dead-letter queue
    channel.start_consuming()

if __name__ == "__main__":
    consume_dead_letter_queue()
