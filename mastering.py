from typing import List

import matchering as mg

from app_config import GENRE_REFERENCES
from logging_config import logger


def master_audio(target: str, genre: str, results: List[mg.Result]) -> None:
    """
    Process audio by matching and mastering the target audio file with the reference audio file for the specified genre.

    :param target: Path to the target audio file.
    :param genre: Music genre to use for the reference audio file.
    :param results: List of mg.Result objects specifying the output formats and options.
    """
    reference = GENRE_REFERENCES.get(genre.lower())
    if not reference:
        logger.error(f"Unsupported genre: {genre}", emoji="❌")
        raise ValueError(f"Unsupported genre: {genre}")

    # Set up logging to capture info and warning messages
    mg.log(info_handler=lambda msg: logger.info(msg, emoji="ℹ️"),
           warning_handler=lambda msg: logger.warning(msg, emoji="⚠️"))

    try:
        # Process the audio files
        mg.process(
            target=target,
            reference=reference,
            results=results
        )
        logger.info("Audio processing completed successfully.", emoji="✅")
    except Exception as e:
        logger.error(f"An error occurred during audio processing: {e}", emoji="❌")
        raise e from None
