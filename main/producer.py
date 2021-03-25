import os
import pika
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) # path to .env on same directory

params = pika.URLParameters(os.getenv('AMQP_URI'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)