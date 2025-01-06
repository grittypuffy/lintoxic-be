from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: int = 201
    message: str = "Uploaded successfully for processing."
