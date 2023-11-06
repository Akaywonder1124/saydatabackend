from ..utils.textextractor import extract_and_recognize_text, get_duration
from tortoise.transactions import in_transaction
from fastapi import APIRouter, UploadFile, Path
from tortoise.queryset import QuerySet
from ..models import MediaFile
from datetime import datetime
import tempfile
import os


router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, file.filename)

    try:
        # Save the uploaded file to the temporary directory
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
        return {"response": "Unsupported file format, try mp4 or wav"}
    # finally:
    #     # Clean up the temporary directory when done
    #     try:
    #         temp_dir.cleanup()
    #     except NotADirectoryError:
    #         # Handle the case when temp_dir is not a directory
    #         return {"response": "Temporary directory is not valid."}


@router.get("/media_files/")
async def get_all_media_files():
    async with in_transaction():
        media_files: QuerySet[MediaFile] = await MediaFile.all()
    return {"response": media_files}


@router.get("/media_files/{media_file_id}")
async def get_media_file_by_id(
    media_file_id: int = Path(..., description="Media File ID")
):
    try:
        media_file = await MediaFile.get(id=media_file_id)
        return {"response": media_file}
    except MediaFile.DoesNotExist:
        return {"response": "Media file not found"}
