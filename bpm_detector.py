from typing import Tuple, List

import librosa

from logging_config import logger


def detect_bpm(file_path: str) -> Tuple[int, List[float]]:
    # Check a file extension
    if not file_path.lower().endswith(('.wav', '.mp3')):
        logger.error("Unsupported file format. Only WAV and MP3 files are supported.", emoji="❌")
        return 0, []

    # Load the audio file
    y, sr = librosa.load(file_path)
    logger.info(f"Audio file loaded with sample rate: {sr}, number of samples: {len(y)}", emoji="ℹ️")

    if len(y) == 0:
        logger.error("Audio file is empty or could not be read.", emoji="❌")
        return 0, []

    # Pre-process the audio to enhance beat detection
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Handle short audio files by adjusting the hop_length parameter
    hop_length = 512 if len(y) > sr else 128

    # Ensure there are enough frames for beat detection
    if len(y) < hop_length:
        logger.warning("Audio file is too short for reliable beat detection.", emoji="⚠️")
        return 0, []

    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr, start_bpm=120, units='time',
                                                 hop_length=hop_length)
    logger.info(f"Tempo detected: {tempo} BPM", emoji="ℹ️")

    if len(beat_frames) == 0:
        logger.warning("No beat frames detected.", emoji="⚠️")
        return 0, []

    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)
    logger.info(f"Beat times: {beat_times}", emoji="ℹ️")

    # Round off the tempo to the nearest whole number
    rounded_tempo = round(tempo)
    logger.info(f"Rounded tempo: {rounded_tempo} BPM", emoji="ℹ️")

    # Return the rounded tempo and beat times
    return rounded_tempo, beat_times


if __name__ == "__main__":
    test_audio_file = 'test/test.mp3'
    detected_tempo, detected_beat_times = detect_bpm(test_audio_file)
    print(f"Estimated tempo: {detected_tempo} BPM")
    print(f"Beat times: {detected_beat_times}")
