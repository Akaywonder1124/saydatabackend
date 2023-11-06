from pydantic import BaseModel, Field
from fastapi import UploadFile


class Media(BaseModel):
    name: str
    file: UploadFile
