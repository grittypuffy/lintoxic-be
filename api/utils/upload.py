from fastapi import UploadFile, File
from api.helpers.filename import get_filename_hash


async def upload_file(file_content: bytes, filename: str, filetype: str):
    hashed_file_name, _ = get_filename_hash(filename)
    if filetype == "text/plain":
        with open(hashed_file_name, "w") as text_file:
            text_file_content = bytes.decode(
                file_content, encoding="utf-8")
            text_file.write(text_file_content)

    else:
        with open(hashed_file_name, "wb") as binary_file:
            binary_file.write(file_content)
    """
    match file.filetype:
        case "image/png" | "image/jpeg":
            pass
        case "text/plain" | "image/jpeg":
            pass
        case "image/png" | "image/jpeg":
            pass
    """
