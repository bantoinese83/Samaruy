import os
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from halo import Halo

from app_config import STEM_OPTIONS, LOCAL_DIR
from audio_separator import AudioSeparator
from logging_config import logger
from model import SeparatedFilesResponse
from utils import validate_file, ensure_directory_exists

router = APIRouter(
    prefix="/api",
    tags=["Stem Separation"]
)

# Ensure the local directory exists
ensure_directory_exists(LOCAL_DIR)


@router.post("/separate/{stem_count}", response_model=SeparatedFilesResponse, status_code=200, summary="Separate Audio")
async def separate_audio(stem_count: int, file: UploadFile = File(...), master: Optional[bool] = False,
                         genre: Optional[str] = None) -> SeparatedFilesResponse:
    logger.debug(
        f"Entering separate_audio with stem_count: {stem_count}, file: {file.filename}, master: {master}, genre: {genre}")
    if stem_count not in STEM_OPTIONS:
        logger.error(f"Invalid stem count: {stem_count}", emoji="❌")
        raise HTTPException(status_code=400,
                            detail=f"Invalid stem count. Please choose from {list(STEM_OPTIONS.keys())}")

    validate_file(file)

    file_location = os.path.join(LOCAL_DIR, file.filename)
    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())
        logger.info(f"File {file.filename} saved to {LOCAL_DIR}", emoji="✅")
    except Exception as e:
        logger.error(f"Failed to save file {file.filename}: {e}", emoji="❌")
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    separator = AudioSeparator(stem_count, master)

    spinner = Halo(text='Separating audio...', spinner='dots')
    spinner.start()
    try:
        separated_files = separator.separate(file.filename, genre)
        if isinstance(separated_files, str):
            logger.error(f"Separation error: {separated_files}", emoji="❌")
            raise HTTPException(status_code=500, detail=separated_files)
        logger.info(f"Separation successful for file {file.filename}", emoji="✅")
        spinner.succeed("Audio separation completed successfully.")
        return SeparatedFilesResponse(
            original_file_name=file.filename,
            stem_count=stem_count,
            separated_files=separated_files
        )
    except Exception as e:
        logger.error(f"An error occurred during separation: {e}", emoji="❌")
        spinner.fail("Audio separation failed.")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_location)
        logger.debug("Exiting separate_audio")


@router.get("/download/{file_name}", response_class=FileResponse, summary="Download Separated Stem")
async def download_stem(file_name: str) -> FileResponse:
    logger.debug(f"Entering download_stem with file_name: {file_name}")
    file_path = os.path.join(LOCAL_DIR, file_name)
    if not os.path.exists(file_path):
        logger.error(f"File {file_name} not found in {LOCAL_DIR}", emoji="❌")
        raise HTTPException(status_code=404, detail="File not found")
    logger.info(f"File {file_name} found, preparing download", emoji="✅")
    logger.debug("Exiting download_stem")
    return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)


@router.get("/search", response_model=List[str], summary="Search and Filter Separated Stems")
async def search_stems(query: Optional[str] = Query(None, description="Search query for file names"),
                       stem_type: Optional[str] = Query(None, description="Filter by stem type"),
                       page: int = Query(1, description="Page number for pagination"),
                       page_size: int = Query(10, description="Number of items per page")) -> List[str]:
    logger.debug(
        f"Entering search_stems with query: {query}, stem_type: {stem_type}, page: {page}, page_size: {page_size}")
    files = []
    for root, _, file_names in os.walk(LOCAL_DIR):
        for file_name in file_names:
            if query and query.lower() not in file_name.lower():
                continue
            if stem_type and stem_type.lower() not in file_name.lower():
                continue
            files.append(file_name)

    total_files = len(files)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_files = files[start:end]

    if not paginated_files:
        logger.info("No files found matching the search criteria", emoji="ℹ️")
    else:
        logger.info(
            f"Found {total_files} files matching the search criteria, returning {len(paginated_files)} files for page {page}",
            emoji="✅")

    logger.debug("Exiting search_stems")
    return paginated_files


@router.get("/stems/{stem_id}", response_model=SeparatedFilesResponse, summary="Get Stem Details")
async def get_stem_details(stem_id: str) -> SeparatedFilesResponse:
    logger.debug(f"Entering get_stem_details with stem_id: {stem_id}")
    file_path = os.path.join(LOCAL_DIR, stem_id)
    if not os.path.exists(file_path):
        logger.error(f"File {stem_id} not found in {LOCAL_DIR}", emoji="❌")
        raise HTTPException(status_code=404, detail="File not found")

    logger.info(f"File {stem_id} found, retrieving details", emoji="✅")

    # Assuming stem_id is the filename of the original file:
    separated_files = []
    for root, _, file_names in os.walk(LOCAL_DIR):
        for file_name in file_names:
            if file_name.startswith(stem_id.split('.')[0]) and file_name != stem_id:  # Exclude the original file
                separated_files.append(file_name)

    if not separated_files:
        logger.error(f"No separated files found for {stem_id}", emoji="❌")
        raise HTTPException(status_code=404, detail="No separated files found")

    stem_count = len(separated_files)

    logger.info(f"File {stem_id} details retrieved successfully", emoji="✅")
    logger.debug("Exiting get_stem_details")
    return SeparatedFilesResponse(
        original_file_name=stem_id,
        stem_count=stem_count,
        separated_files=separated_files
    )


@router.get("/stems", response_model=List[str], summary="Get All Stems")
async def get_all_stems() -> List[str]:
    logger.debug("Entering get_all_stems")
    files = []
    for root, _, file_names in os.walk(LOCAL_DIR):
        for file_name in file_names:
            files.append(file_name)

    if not files:
        logger.info("No stems found", emoji="ℹ️")
    else:
        logger.info(f"Found {len(files)} stems", emoji="✅")

    logger.debug("Exiting get_all_stems")
    return files
