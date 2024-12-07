from confluent_kafka import Consumer, Producer

def setup_kafka_consumer(bootstrap_servers, group_id, topic):
    """
    Set up Kafka consumer.
    """
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    return consumer

def setup_kafka_producer(bootstrap_servers):
    """
    Set up Kafka producer.
    """
    return Producer({'bootstrap.servers': bootstrap_servers})
