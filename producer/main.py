import json
import os
from time import sleep

from faker import Faker
from kafka import KafkaProducer
from vehicle_provider import VehicleProvider

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
DETECTIONS_PER_SECOND = float(os.environ.get("DETECTIONS_PER_SECOND"))
SLEEP_TIME = 1 / DETECTIONS_PER_SECOND

fake = Faker()
fake.add_provider(VehicleProvider)

if __name__ == "__main__":

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        detection: dict = fake.vehicle_object()
        producer.send(DETECTIONS_TOPIC, value=detection)
        print(detection)  # DEBUG
        sleep(SLEEP_TIME)

    producer.flush()
