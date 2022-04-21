import asyncio
import json
import logging

from beanie import init_beanie
from config import settings
from kafka import KafkaConsumer, KafkaProducer
from models import VehicleDetection
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError


async def database_connection():
    client = AsyncIOMotorClient(
        f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"
    )

    await init_beanie(database=client[settings.mongo_database], document_models=[VehicleDetection])


async def run():
    await database_connection()

    consumer = KafkaConsumer(
        settings.detections_topic,
        bootstrap_servers=settings.kafka_broker_url,
        group_id="vehicle_detector",
        value_deserializer=lambda value: json.loads(value.decode("UTF-8")),
        enable_auto_commit=True,
    )

    producer = KafkaProducer(
        bootstrap_servers=settings.kafka_broker_url,
        value_serializer=lambda value: json.dumps(value).encode(),
        retries=5,
    )

    for message in consumer:
        try:
            detection = VehicleDetection.parse_obj(message.value)
        except ValidationError:
            logging.exception(f"Invalid detection message: {str(message.value)}")

        print(message.value)

        try:
            await detection.insert()
        except Exception:
            logging.exception(f"Error inserting detection: {str(message.value)}")

        if message.value.get("Category") == settings.suspicious_vehicle:
            try:
                producer.send(settings.alerts_topic, message.value)
            except Exception:
                logging.exception(f"Error sending alert: {str(message.value)}")


if __name__ == "__main__":
    asyncio.run(run())
