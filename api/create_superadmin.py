import argparse
import asyncio

from beanie import init_beanie
from config import settings
from models.db import User
from motor.motor_asyncio import AsyncIOMotorClient
from utils.security import pwd_context


async def main(username: str, password: str):
    try:

        client = AsyncIOMotorClient(
            f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"
        )

        await init_beanie(database=client[settings.mongo_database], document_models=[User])

        user = User(username=username, password=pwd_context.hash(password), role="superadmin")
        await user.insert()
        print("Superuser created!")
    except Exception as e:
        print(f"Error creating superuser: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str, required=True)
    parser.add_argument("--password", type=str, required=True)

    args = parser.parse_args()
    asyncio.run(main(args.username, args.password))
