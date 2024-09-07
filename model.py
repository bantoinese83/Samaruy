from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator


class SeparatedFilesResponse(BaseModel):
    original_file_name: str = Field(..., description="The name of the original uploaded file")
    stem_count: int = Field(..., description="The number of stems the audio was separated into")
    separated_files: List[str] = Field(..., description="List of separated file names")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the separation process")

    @field_validator('stem_count')
    def validate_stem_count(cls, value):
        if value not in {2, 4, 5}:
            raise ValueError('Invalid stem count. Must be one of 2, 4, or 5.')
        return value

    @field_validator('separated_files')
    def validate_separated_files(cls, value):
        if not value:
            raise ValueError('Separated files list cannot be empty.')
        return value
