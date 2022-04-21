import logging

from fastapi import APIRouter, Depends, HTTPException, status
from models.db import VehicleDetection
from models.routers import User
from utils.security import get_current_user

detections_router = APIRouter(
    prefix="/detections",
    tags=["detections"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "NOT FOUND"}},
)


@detections_router.get("")
async def detections(skip: int = 0, limit: int = 20, current_user: User = Depends(get_current_user)):
    vehicles = []
    try:
        vehicles = await VehicleDetection.all().skip(skip).limit(limit).to_list()
    except Exception:
        logging.exception("Error getting detections")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error getting detections")
    return vehicles
