import json
import pika
from workflows.install_client import start as install_client
from workflows.check_segment import start as check_segment

def callback(ch, method, properties, body):
    try:
        body = body.decode()
        print("[x] received %r" % body)
        data = json.loads(body)
        
        computer_name = data.get('computer_name')
        type = data.get('type')
        id=data.get('_id')
        print(str(id))
        if type =='client install':
            print("shakedi info")
            install_client(computer_name=computer_name)
        #workflowinfo(country_name=country_name,computer_name=computer_name)
        elif type == "check segment":
            check_segment(ip_address=computer_name,id=id)
        #workflownasa(country_name=country_name,computer_name=computer_name)
        else:
            raise Exception("Invalid workflow")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        

    except Exception as e:
            print(f"Error processing message: {e}. Skipping message.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)



def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Step 1: Declare the Dead-Letter Queue
    channel.queue_declare(queue='dead_letter_queue', durable=True)

    # Step 2: Declare the Dead-Letter Exchange
    channel.exchange_declare(exchange='dead_letter_exchange', exchange_type='direct',durable=True)

    # Bind the dead-letter queue to the dead-letter exchange
    channel.queue_bind(exchange='dead_letter_exchange', queue='dead_letter_queue')

    # Step 3: Declare the Main Queue with Dead-Letter Exchange
    args = {
        'x-dead-letter-exchange': 'dead_letter_exchange',  # Link to the dead-letter exchange
        'x-dead-letter-routing-key': 'dead_letter_queue',    # Optionally, set a routing key
        'x-message-ttl': 60000  # Optional: TTL (in milliseconds) for messages in the main queue
    }

    channel.queue_declare(queue="process", durable=True, arguments=args)
    channel.basic_consume(queue="process", on_message_callback=callback)
    print("waiting for messages...")
    channel.start_consuming()

consume()
