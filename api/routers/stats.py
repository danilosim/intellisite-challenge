import logging

from fastapi import APIRouter, Depends, HTTPException, status
from models.db import VehicleDetection
from models.routers import User
from utils.security import get_current_user

stats_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "NOT FOUND"}},
)


@stats_router.get("")
async def stats(current_user: User = Depends(get_current_user)):
    stats = []

    try:
        stats = await VehicleDetection.aggregate([{"$group": {"_id": "$Make", "count": {"$sum": 1}}}]).to_list()
    except Exception:
        logging.exception("Error getting stats")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error getting stats")

    return {k["_id"]: k["count"] for k in stats}
