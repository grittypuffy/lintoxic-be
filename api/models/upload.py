from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: int = 202
    message: str = "Uploaded successfully for processing."


class UploadContent(BaseModel):
    content: str
