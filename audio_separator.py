import os
from datetime import datetime
from io import BytesIO
from typing import List, Union, Optional

import matchering as mg
from spleeter.separator import Separator

from app_config import STEM_OPTIONS, LOCAL_DIR
from bpm_detector import detect_bpm
from file_manager import File_Manager
from key_detector import key_detect
from logging_config import logger
from mastering import master_audio


class AudioSeparator:
    def __init__(self, stem_count: int, master: Optional[bool] = False):
        logger.debug(f"Initializing AudioSeparator with stem_count: {stem_count}, master: {master}")
        if stem_count not in STEM_OPTIONS:
            raise ValueError(f'Invalid stem count. Please choose from {list(STEM_OPTIONS.keys())}')
        self.model_configuration = STEM_OPTIONS[stem_count]
        self.separator = Separator(self.model_configuration)
        self.file_manager = File_Manager()
        self.master = master
        logger.debug("Exiting __init__")

    def separate(self, file_name: str, genre: Optional[str] = None) -> Union[List[str], str]:
        logger.debug(f"Starting separation for file: {file_name}")
        try:
            audio_file = self.download_file(file_name)
            temp_audio_file_path = self.save_temp_file(file_name, audio_file)
            output_dir = self.create_output_dir()
            self.perform_separation(temp_audio_file_path, output_dir)
            audio_data = self.collect_separated_files(output_dir)

            # Detect BPM and Key
            bpm = self.detect_bpm(temp_audio_file_path)
            key = self.detect_key(temp_audio_file_path)
            logger.info(f"Detected BPM: {bpm}, Detected Key: {key}", emoji="ℹ️")

            separated_file_paths = self.save_separated_files(audio_data, file_name, bpm, key)

            # Optionally master the audio
            if self.master and genre:
                self.master_audio(temp_audio_file_path, genre, separated_file_paths)

            logger.debug(f"Separation completed successfully for file: {file_name}")
            return separated_file_paths
        except Exception as e:
            logger.error(f'An error occurred during separation: {e}', emoji="❌")
            return 'An error occurred during the separation process.'
        finally:
            logger.debug("Exiting separate")

    def download_file(self, file_name: str) -> BytesIO:
        logger.debug(f"Downloading file: {file_name} from directory: {LOCAL_DIR}")
        audio_file = self.file_manager.download_from_directory(file_name, LOCAL_DIR)
        if not audio_file:
            raise Exception('Failed to download the audio file from local directory.')
        logger.debug("Exiting download_file")
        return audio_file

    @staticmethod
    def save_temp_file(file_name: str, audio_file: BytesIO) -> str:
        temp_audio_file_path = f"/tmp/{file_name}"
        logger.debug(f"Saving temporary file: {temp_audio_file_path}")
        with open(temp_audio_file_path, 'wb') as temp_file:
            temp_file.write(audio_file.read())
        logger.debug("Exiting save_temp_file")
        return temp_audio_file_path

    @staticmethod
    def create_output_dir() -> str:
        output_dir = '/tmp/output'
        logger.debug(f"Creating output directory: {output_dir}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logger.debug("Exiting create_output_dir")
        return output_dir

    def perform_separation(self, temp_audio_file_path: str, output_dir: str) -> None:
        logger.debug(f"Performing separation on file: {temp_audio_file_path} to directory: {output_dir}")
        self.separator.separate_to_file(temp_audio_file_path, output_dir)
        logger.debug("Exiting perform_separation")

    @staticmethod
    def collect_separated_files(output_dir: str) -> dict:
        logger.debug(f"Collecting separated files from directory: {output_dir}")
        audio_data = {}
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    file_data = BytesIO(f.read())
                    audio_data[file] = file_data
        logger.debug("Exiting collect_separated_files")
        return audio_data

    def save_separated_files(self, audio_data: dict, original_file_name: str, bpm: int, key: str) -> List[str]:
        logger.debug(f"Saving separated files for original file: {original_file_name}")
        separated_file_paths = []
        base_name = os.path.splitext(original_file_name)[0]

        for file_name, file_data in audio_data.items():
            stem_type: str = file_name.split('.')[0]  # Assuming a file name format indicates a stem type
            subdirectory: str = os.path.join(LOCAL_DIR, stem_type)
            local_separated_file_name = f"{base_name}_{stem_type}_BPM{bpm}_Key{key}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp3"
            logger.debug(f"Saving file: {local_separated_file_name} to directory: {subdirectory}")
            self.file_manager.save_to_directory(file_data, local_separated_file_name, subdirectory)
            separated_file_paths.append(local_separated_file_name)
        logger.debug("Exiting save_separated_files")
        return separated_file_paths

    @staticmethod
    def detect_bpm(file_path: str) -> int:
        logger.debug(f"Detecting BPM for file: {file_path}")
        bpm, _ = detect_bpm(file_path)
        logger.debug(f"Detected BPM: {bpm}")
        return bpm

    @staticmethod
    def detect_key(file_path: str) -> str:
        logger.debug(f"Detecting key for file: {file_path}")
        key = key_detect(file_path)
        logger.debug(f"Detected key: {key}")
        return key

    @staticmethod
    def master_audio(target: str, genre: str, results: List[str]) -> None:
        logger.debug(f"Mastering audio for target: {target}, genre: {genre}")
        master_audio(target, genre, [mg.pcm16(result) for result in results])
        logger.debug("Exiting master_audio")
