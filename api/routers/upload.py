import logging
from typing import List
import uuid
import time

from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse

from api.models.upload import UploadResponse, UploadContent
from api.config import AppConfig, get_config
from api.utils.upload import upload_file
import api.utils as utils

router = APIRouter()

config = AppConfig()


@router.post("/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile) -> UploadResponse:
    try:
        timestamp = int(time.time())
        if file.content_type not in ["audio/mpeg", "audio/ogg", "audio/x-flac", "image/jpeg", "image/png", "text/plain", "audio/wav", "audio/flac", "video/mpeg"]:
            return Exception(f"The file of type {file.content_type} is not accepted")
        file_content = await file.read()
        process_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        background_tasks.add_task(
            utils.upload.upload_file, file_content, file.filename, file.content_type, process_id, user_id, timestamp)
        upload_response = UploadResponse()
        return JSONResponse(content=upload_response.dict(), status_code=201)
    except Exception as e:
        logging.error(e)
        upload_response = UploadResponse(
            status=422, message=f"The file was not processed successfully: {str(e)}")
        return JSONResponse(content=upload_response.dict(), status_code=422)


@router.post("/content")
async def upload_file(background_tasks: BackgroundTasks, content: UploadContent) -> UploadResponse:
    try:
        timestamp = int(time.time())
        process_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        background_tasks.add_task(
            utils.upload.upload_content, content.content, process_id, user_id, timestamp)
        upload_response = UploadResponse()
        return JSONResponse(content=upload_response.dict(), status_code=201)
    except Exception as e:
        logging.error(e)
        upload_response = UploadResponse(
            status=422, message=f"The file was not processed successfully: {str(e)}")
        return JSONResponse(content=upload_response.dict(), status_code=422)


@router.get("/{upload_id}")
async def get_upload_status(upload_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
