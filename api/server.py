import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from api.constants import cors_allowed_headers, cors_allowed_methods

from api.routers.api.v1 import router as v1_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_methods=cors_allowed_methods,
    allow_headers=cors_allowed_headers,
    expose_headers=["*"],
    allow_credentials=True
)

app.include_router(v1_router, prefix="/api/v1")
