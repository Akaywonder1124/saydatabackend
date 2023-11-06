from ..utils.textextractor import extract_and_recognize_text, get_duration
from tortoise.transactions import in_transaction
from fastapi import APIRouter, UploadFile
from tortoise.queryset import QuerySet
from ..models import MediaFile
from datetime import datetime
import tempfile
import os


router = APIRouter()

# Set the temporary directory for moviepy


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    temp_dir = tempfile.TemporaryDirectory()

    try:
        # Save the uploaded file to the temporary directory
        temp_file_path = os.path.join(temp_dir.name, file.filename)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())
            text = extract_and_recognize_text(temp_file_path)
            file_duration = get_duration(temp_file_path)

            # save to db
            file_db = await MediaFile.create(
                name=file.filename,
                text=text,
                file_type=file.filename.split(".")[1],
                duration=f"{file_duration}" + "seconds",
                date_created=datetime.utcnow(),
            )
            return {"response": "File transcribed successfully"}
    except Exception:
        return {response: f"error{Exception}"}
    finally:
        # Clean up the temporary directory when done
        temp_dir.cleanup()


@router.get("/media_files/")
async def get_all_media_files():
    async with in_transaction():
        media_files: QuerySet[MediaFile] = await MediaFile.all()
    return {"response": media_files}
