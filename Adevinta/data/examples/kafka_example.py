from kafka_example import KafkaProducer, KafkaConsumer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {'user_id': '12345', 'event': 'purchase', 'amount': 99.99}
producer.send('ecommerce_events', value=data)
producer.flush()
#------------------------------

consumer = KafkaConsumer(
    'ecommerce_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    event = message.value
    print(f"Received event: {event}")