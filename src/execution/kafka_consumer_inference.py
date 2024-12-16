import os
import json
import logging
import pandas as pd
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.execution.model_loader import load_model
from src.execution.inference import predict
from src.execution.trade_execution import send_order_to_broker
from src.utils.logging import setup_logger
from src.database.models import StockDataPrediction

# Logger setup
logger = setup_logger(
    name="kafka-consumer-inference",
    log_file="logs/consumer_inference.log",
    level=logging.DEBUG,
    file_log_level=logging.DEBUG,
    console_log_level=logging.INFO
)

# Environment Configuration
RAW_TOPIC = "processed-stock-data"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER")
MODEL_BUCKET = "trained-models"
BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_API_SECRET = os.getenv("BROKER_API_SECRET")
BROKER_API_URL = os.getenv("BROKER_API_URL", "https://paper-api.alpaca.markets")
POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")

# Kafka Consumer setup
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': 'inference-group',
    'auto.offset.reset': 'earliest'
})

# SQLAlchemy session setup
engine = create_engine(POSTGRES_CONN_STRING)
Session = sessionmaker(bind=engine)
session = Session()

def save_prediction_to_db(predicted_data):
    """
    Save predicted data to the stock_data_prediction table.

    Args:
        predicted_data (dict): Predicted data to be stored.
    """
    try:
        new_prediction = StockDataPrediction(
            symbol=predicted_data["symbol"],
            price=predicted_data["price"],
            size=predicted_data["size"],
            timestamp=predicted_data["timestamp"],
            rolling_mean_200=predicted_data.get("rolling_mean_200"),
            rolling_std_200=predicted_data.get("rolling_std_200"),
            target=predicted_data.get("target"),
            prediction=predicted_data["prediction"],
        )
        session.add(new_prediction)
        session.commit()
        logger.info(f"Saved prediction to DB: {predicted_data}")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to save prediction to DB: {e}")

def handle_message(message, model):
    """
    Process incoming Kafka messages, make predictions, save to DB, and send trades to the broker.

    Args:
        message: Kafka message object.
        model: The loaded prediction model.
    """
    logger.info(f"Raw message value: {message.value()}")

    try:
        # Parse the input message
        input_data = json.loads(message.value().decode('utf-8'))
        input_df = pd.DataFrame([input_data])
        logger.info(f"Received input data: {input_df}")

        # Make predictions using the model
        predictions = predict(model, input_df)
        prediction = predictions[0]  # Access the first prediction value
        logger.info(f"Prediction: {prediction}")

        # Combine input data with the prediction
        predicted_data = {
            "symbol": input_data["symbol"],
            "price": input_data["price"],
            "size": input_data["size"],
            "timestamp": input_data["timestamp"],
            "rolling_mean_200": input_data.get("rolling_mean_200"),
            "rolling_std_200": input_data.get("rolling_std_200"),
            "target": input_data.get("target"),
            "prediction": prediction
        }

        # Save the prediction to the database
        save_prediction_to_db(predicted_data)

        # Send a trade order to the broker
        side = "buy" if prediction > 0 else "sell"
        qty = 1  # Adjust as needed for trade quantity
        logger.info(f"Sending order to broker: {side} {qty} shares of {predicted_data['symbol']}.")
        response = send_order_to_broker(
            api_key=BROKER_API_KEY,
            secret_key=BROKER_API_SECRET,
            base_url=BROKER_API_URL,
            symbol=predicted_data["symbol"],
            qty=qty,
            side=side
        )
        logger.info(f"Broker response: {response}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main():
    """
    Main loop for the outbound Kafka consumer.
    """
    logger.info("Loading the latest model from storage...")
    model = load_model(MODEL_BUCKET)

    # Subscribe to the Kafka topic
    consumer.subscribe([RAW_TOPIC])
    logger.info(f"Subscribed to Kafka topic {RAW_TOPIC}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    break
            handle_message(msg, model)
    finally:
        consumer.close()
        session.close()

if __name__ == "__main__":
    main()
