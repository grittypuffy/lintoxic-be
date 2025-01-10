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
import api.utils as utils
# from api.workers.upload import upload_file as upload_file_task
# from api.workers.upload import upload_content as upload_content_task

router = APIRouter()

config = AppConfig()


@router.post("/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile) -> UploadResponse:
    try:
        timestamp = int(time.time())
        if file.content_type not in ["video/mp4", "audio/mpeg", "audio/ogg", "audio/x-flac", "image/jpeg", "image/png", "text/plain", "audio/wav", "audio/flac", "video/mpeg"]:
            return Exception(f"The file of type {file.content_type} is not accepted")
        file_content = await file.read()
        process_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        '''
        upload_file_task.apply_async(
            file_content, file.filename, file.content_type, process_id, user_id, timestamp)
        '''
        background_tasks.add_task(
            utils.upload.upload_file, file_content, file.filename, file.content_type, process_id, user_id, timestamp)
        upload_response = UploadResponse()
        return JSONResponse(content=upload_response.dict(), status_code=202)
    except Exception as e:
        logging.error(e)
        upload_response = UploadResponse(
            status=422, message=f"The file was not processed successfully: {str(e)}")
        return JSONResponse(content=upload_response.dict(), status_code=422)


@router.post("/content")
async def upload_content(background_tasks: BackgroundTasks, content: UploadContent) -> UploadResponse:
    try:
        timestamp = int(time.time())
        process_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        '''
        task_id = upload_content_task.apply_async(
            kwargs={
                'content': content.content,
                'process_id': process_id,
                'user_id': user_id,
                'timestamp': timestamp
            })
        print(task_id)
        '''
        background_tasks.add_task(
            utils.upload.upload_content, content.content, process_id, user_id, timestamp)
        upload_response = UploadResponse()
        return JSONResponse(content=upload_response.dict(), status_code=202)
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
