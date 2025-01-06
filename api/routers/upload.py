from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from api.models.upload import UploadResponse
from api.config import AppConfig, get_config
from typing import List
from api.utils.upload import upload_file
import api.utils as utils
import logging

router = APIRouter()

config = AppConfig()


@router.post("/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile) -> UploadResponse:
    try:
        file_content = await file.read()
        background_tasks.add_task(
            utils.upload.upload_file, file_content, file.filename, file.content_type)
        upload_response = UploadResponse()
        return JSONResponse(content=upload_response.dict(), status_code=201)
    except Exception as e:
        logging.error(e)
        upload_response = UploadResponse(
            status=422, message="The file was not processed successfully")
        return JSONResponse(content=upload_response.dict(), status_code=422)


@router.get("/{upload_id}")
async def get_upload_status(upload_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
