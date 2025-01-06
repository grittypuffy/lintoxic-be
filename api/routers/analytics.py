from fastapi import APIRouter, HTTPException
# from models.analytics import Analytics
from api.config import AppConfig, get_config
from typing import List

router = APIRouter()

config = AppConfig()


@router.get("/")
async def get_analytics():
    try:
        analytics_collection = config.db["logs"]
        total_uploads = len(await analytics_collection.find().to_list())
        total_toxicity = len(await analytics_collection.find({"results.toxicity": True}).to_list())
        total_accuracy = len(await analytics_collection.find({"results.accuracy": True}).to_list())
        total_nsfw = len(await analytics_collection.find({"results.nsfw": True}).to_list())
        return {"total_uploads": total_uploads, "total_toxicity": total_toxicity, "total_accuracy": total_accuracy, "total_nsfw": total_nsfw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
