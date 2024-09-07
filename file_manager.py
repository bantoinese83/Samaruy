import os
import time
from io import BytesIO
from typing import Optional

from logging_config import logger


class File_Manager:
    @staticmethod
    def download_from_directory(file_name: str, directory: str) -> Optional[BytesIO]:
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            logger.error(f"The file {file_name} does not exist in the directory {directory}.", emoji="❌")
            raise FileNotFoundError(f"The file {file_name} does not exist in the directory {directory}.")
        try:
            with open(file_path, 'rb') as file:
                logger.info(f"Successfully downloaded {file_name} from {directory}.", emoji="✅")
                return BytesIO(file.read())
        except Exception as e:
            logger.error(f"An error occurred while reading the file {file_name}: {e}", emoji="❌")
            raise IOError(f"An error occurred while reading the file {file_name}: {e}")

    @staticmethod
    def save_to_directory(file_data: BytesIO, file_name: str, directory: str):
        if not isinstance(file_data, BytesIO):
            logger.error("file_data must be of type BytesIO", emoji="❌")
            raise ValueError("file_data must be of type BytesIO")
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory {directory}.", emoji="✅")
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'wb') as file:
                file.write(file_data.read())
                logger.info(f"Successfully saved {file_name} to {directory}.", emoji="✅")
        except Exception as e:
            logger.error(f"An error occurred while writing the file {file_name}: {e}", emoji="❌")
            raise IOError(f"An error occurred while writing the file {file_name}: {e}")

    @staticmethod
    def cleanup_directory(directory: str, days_old: int = 7):
        if not os.path.exists(directory):
            logger.info(f"Directory {directory} does not exist. No cleanup needed.", emoji="ℹ️")
            return
        now = time.time()
        cutoff = now - (days_old * 86400)  # 86400 seconds in a day
        print(f"Files found in directory: {os.listdir(directory)}")
        for filename in os.listdir(directory):
            print(f"Checking file: {filename}") # Add this line
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff:
                print(f"Deleting file: {filename}") # Add this line
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted {filename} from {directory}.", emoji="✅")
                except Exception as e:
                    logger.error(f"An error occurred while deleting the file {filename}: {e}", emoji="❌")
                    raise IOError(f"An error occurred while deleting the file {filename}: {e}")