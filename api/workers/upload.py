import os
from typing import Optional
from celery import shared_task

from api.helpers.filename import get_filename_hash
from api.config import AppConfig, get_config
from api.services.validate import evaluate_audio, evaluate_image, evaluate_text, evaluate_video
from api.utils.email import send_email
from api.utils.upload import insert_log, update_log
from api.config.celery import get_celery_instance

app = get_celery_instance()

config: AppConfig = get_config()


@shared_task(ignore_result=False)
async def upload_file(file_content: bytes, filename: str, filetype: str, process_id: str, user_id: str, timestamp: int):
    hashed_file_name, _ = get_filename_hash(filename)
    hashed_file_path = os.path.join(config.env.upload_dir, hashed_file_name)
    pending_insertion_id = await insert_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                            completed=False, filename=filename, filetype=filetype, content=None, result=None)
    pending_insertion_id = str(pending_insertion_id.inserted_id)

    if filetype == "text/plain":
        with open(hashed_file_path, "w") as text_file:
            text_file_content = bytes.decode(
                file_content, encoding="utf-8")
            text_file.write(text_file_content)

    else:
        with open(hashed_file_path, "wb") as binary_file:
            binary_file.write(file_content)

    match filetype:
        case "image/png" | "image/jpeg":
            result = await evaluate_image(hashed_file_path)
            if result.get("status"):
                insertion_id = await update_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                                completed=True, filename=filename, filetype=filetype, content=None, result=result, object_id=pending_insertion_id)
                return result

        case "text/plain":
            text_file_content = bytes.decode(
                file_content, encoding="utf-8")
            result = await evaluate_text(text_file_content)
            if result.get("status"):
                insertion_id = await update_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                                completed=True, filename=filename, filetype=filetype, content=None, result=result, object_id=pending_insertion_id)
                return result

        case "audio/wav" | "audio/flac" | "audio/mpeg" | "audio/x-flac":
            result = await evaluate_audio(hashed_file_path)
            if result.get("status"):
                insertion_id = await update_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                                completed=True, filename=filename, filetype=filetype, content=None, result=result, object_id=pending_insertion_id)
                return result

        case "video/mpeg" | "video/mp4":
            result = await evaluate_video(hashed_file_path)
            if result.get("status"):
                insertion_id = await update_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                                completed=True, filename=filename, filetype=filetype, content=None, result=result, object_id=pending_insertion_id)
                return result


@shared_task(ignore_result=False)
async def upload_content(content: str, process_id: str, user_id: str, timestamp: int):
    pending_insertion_id = await insert_log(timestamp, user_id, process_id,
                                            False, None, None, content, None)
    result = await evaluate_text(content)
    if result.get("status"):
        insertion_id = await update_log(timestamp, user_id, process_id,
                                        True, None, None, content, result, str(pending_insertion_id.inserted_id))
    return result
