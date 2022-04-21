import routers
from beanie import init_beanie
from config import settings
from fastapi import FastAPI
from models.db import User, VehicleDetection
from motor.motor_asyncio import AsyncIOMotorClient


def create_app():

    app = FastAPI(
        openapi_url="/swagger.json",
        docs_url="/",
        redoc_url=None,
    )

    app.include_router(routers.alerts_router)
    app.include_router(routers.detections_router)
    app.include_router(routers.stats_router)
    app.include_router(routers.users_router)
    app.include_router(routers.auth_router)

    @app.on_event("startup")
    async def app_init():
        client = AsyncIOMotorClient(
            f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"
        )

        await init_beanie(database=client[settings.mongo_database], document_models=[VehicleDetection, User])

    return app


app = create_app()
