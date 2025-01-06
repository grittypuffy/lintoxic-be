from fastapi import APIRouter, HTTPException
# from api.models.analytics import Analytics
from api.config import AppConfig, get_config
from typing import List

router = APIRouter()

config = AppConfig()


@router.get("/")
async def get_logs():
    try:
        log_collection = config.db["logs"]
        data = await log_collection.find().to_list()
        for log in data:
            log["_id"] = str(log["_id"])
        return {"logs": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
