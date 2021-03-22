import os
import pika
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) # path to .env on same directory

params = pika.URLParameters(os.getenv('AMQP_URI'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Received in main')
    print(body)

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()