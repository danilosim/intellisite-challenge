import json

from config import settings
from fastapi import APIRouter, Depends, Request, status
from kafka import KafkaConsumer
from models.routers import User
from sse_starlette.sse import EventSourceResponse
from utils.security import get_current_user

alerts_router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "NOT FOUND"}},
)


@alerts_router.get("")
# async def alerts(request: Request, current_user: User = Depends(get_current_user)):
async def alerts(request: Request):
    consumer = KafkaConsumer(
        settings.alerts_topic,
        bootstrap_servers=settings.kafka_broker_url,
        value_deserializer=lambda value: json.loads(value.decode("UTF-8")),
    )

    def get_alert():
        for message in consumer:
            yield message.value

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            alert = next(get_alert(), None)

            yield json.dumps(alert)

    return EventSourceResponse(event_generator())
