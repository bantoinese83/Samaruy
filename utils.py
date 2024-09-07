import os

from fastapi import UploadFile, HTTPException

from app_config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from logging_config import logger


def validate_file(file: UploadFile) -> None:
    """
    Validate the uploaded file.

    :param file: Uploaded audio file.
    :raises HTTPException: If the file is invalid.
    """
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            logger.error(f"Invalid file extension: {file_extension}", emoji="❌")
            raise HTTPException(status_code=400, detail="Invalid file extension. Allowed extensions are .mp3, .wav")

        file_size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)  # Reset a file pointer after reading
        if file_size_mb > MAX_FILE_SIZE_MB:
            logger.error(f"File size exceeds limit: {file_size_mb} MB", emoji="❌")
            raise HTTPException(status_code=400, detail=f"File size exceeds limit of {MAX_FILE_SIZE_MB} MB")

        logger.info(f"File {file.filename} validated successfully", emoji="✅")
    except HTTPException as e:
        logger.error(f"Validation error: {e.detail}", emoji="❌")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file validation: {e}", emoji="❌")
        raise HTTPException(status_code=500, detail="Internal server error during file validation")


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure the specified directory exists, create it if it does not.

    :param directory: Directory path to check or create.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory {directory}", emoji="✅")
        else:
            logger.info(f"Directory {directory} already exists", emoji="ℹ️")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}", emoji="❌")
        raise