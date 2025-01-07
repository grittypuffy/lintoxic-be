import os
from typing import Optional
from api.helpers.filename import get_filename_hash
from api.config import AppConfig, get_config
from api.services.validate import evaluate_audio, evaluate_image, evaluate_text, evaluate_video
from api.utils.email import send_email

import bson


config: AppConfig = get_config()


async def insert_log(timestamp: int, user_id: str, process_id: str, completed: bool, filename: Optional[str], filetype: Optional[str], content: Optional[str], result: Optional[dict]):
    db_document = {
        "timestamp": timestamp,
        "user_id": user_id,
        "process_id": process_id,
        "completed": True,
        "filename": filename,
        "filetype": filetype,
        "content": None,
        "results": {
            "harmful": True,
            "toxicity": result.get("toxicity", False),
            "accuracy": result.get("accuracy", False),
            "nsfw": result.get("nsfw", False),
            "reason": result.get("reason"),
            "labels": result.get("labels", None)
        } if result else None
    }
    db_result = await config.db["logs"].insert_one(db_document)
    return db_result


async def update_log(timestamp: int, user_id: str, process_id: str, completed: bool, filename: Optional[str], filetype: Optional[str], content: Optional[str], result: Optional[dict], object_id: str):
    db_document = {
        "timestamp": timestamp,
        "user_id": user_id,
        "process_id": process_id,
        "completed": True,
        "filename": filename,
        "filetype": filetype,
        "content": None,
        "results": {
            "harmful": True,
            "toxicity": result.get("toxicity", False),
            "accuracy": result.get("accuracy", False),
            "nsfw": result.get("nsfw", False),
            "reason": result.get("reason"),
            "labels": result.get("labels", None)
        } if result else None
    }
    db_result = await config.db["logs"].update_one({"_id": bson.objectid.ObjectId(object_id)}, {"$set": db_document})
    violation_record = await config.db["violations"].find_one({"user_id": user_id})
    violations = violation_record.get("violations", 0) + 1
    if (v_id := violation_record.get("_id")):
        db_result = await config.db["violations"].update_one({"_id": v_id}, {"$set": {"violation": violation_record.get("violations") + 1, "records": violation_record.get("records").append(db_document)}})
    else:
        db_result = await config.db["violations"].insert_one({"user_id": user_id, "violation": 1, "records": [db_document]})
    if violations > 5:
        send_email(user_id, violations)
    return db_result


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
                insertion_id = await_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                         completed=True, filename=filename, filetype=filetype, content=None, result=result, object_id=pending_insertion_id)
                return result


async def upload_content(content: str, process_id: str, user_id: str, timestamp: int):
    pending_insertion_id = await insert_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                            completed=False, filename=None, filetype=None, content=content, result=None)
    result = await evaluate_text(content)
    if result.get("status"):
        insertion_id = await update_log(timestamp=timestamp, user_id=user_id, process_id=process_id,
                                        completed=True, filename=None, filetype=None, content=content, result=result, object_id=pending_insertion_id)
    return result
