from fastapi import APIRouter, HTTPException
# from models.analytics import Analytics
from api.config import AppConfig, get_config
from typing import List

router = APIRouter()

config = AppConfig()


@router.get("/")
async def get_analytics():
    try:
        analytics_collection = config.db["analytics"]
        data = await analytics_collection.find().to_list()
        return {"analytics": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
