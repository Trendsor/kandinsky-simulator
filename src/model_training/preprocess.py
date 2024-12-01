from confluent_kafka import Consumer, KafkaError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

