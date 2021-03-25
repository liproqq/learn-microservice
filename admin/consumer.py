import pika, django, json, environ, os


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
# import Product after django setup so it's recognized as a model
from products.models import Product

params = pika.URLParameters(env('AMQP_URI'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('product likes incremented')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()