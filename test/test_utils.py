import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock

from fastapi import UploadFile, HTTPException

from app_config import MAX_FILE_SIZE_MB
from utils import validate_file, ensure_directory_exists


class TestUtils(unittest.TestCase):

    @patch('utils.logger')
    def test_validate_file_valid(self, mock_logger):
        file = UploadFile(filename="test.mp3", file=BytesIO(b"Test data" * 1024 * 1024))  # 1 MB file
        validate_file(file)
        mock_logger.info.assert_called_with(f"File {file.filename} validated successfully", emoji="✅")

    @patch('utils.logger')
    def test_validate_file_invalid_extension(self, mock_logger):
        file = MagicMock(spec=UploadFile)
        file.filename = 'test.txt'
        file.file = MagicMock()
        file.file.read.return_value = b''

        with self.assertRaises(HTTPException) as context:
            validate_file(file)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Invalid file extension. Allowed extensions are .mp3, .wav")
        mock_logger.error.assert_called_with(
            "Validation error: Invalid file extension. Allowed extensions are .mp3, .wav",
            emoji="❌")  # Corrected assertion

    @patch('utils.logger')
    def test_validate_file_exceeds_size(self, mock_logger):
        file = MagicMock(spec=UploadFile)
        file.filename = 'test.mp3'
        file.file = MagicMock()
        file.file.read.return_value = b'a' * (MAX_FILE_SIZE_MB * 1024 * 1024 + 1)

        with self.assertRaises(HTTPException) as context:
            validate_file(file)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, f"File size exceeds limit of {MAX_FILE_SIZE_MB} MB")
        mock_logger.error.assert_called_with(f"Validation error: File size exceeds limit of {MAX_FILE_SIZE_MB} MB",
                                             emoji="❌")  # Corrected assertion

    @patch('utils.logger')
    def test_validate_file_unexpected_error(self, mock_logger):
        file = UploadFile(filename="test.mp3", file=BytesIO(b"Test data"))
        with patch('os.path.splitext', side_effect=Exception("Unexpected error")):
            with self.assertRaises(HTTPException) as context:
                validate_file(file)
            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "Internal server error during file validation")
            mock_logger.error.assert_called_with("Unexpected error during file validation: Unexpected error", emoji="❌")

    @patch('utils.logger')
    @patch('os.makedirs')
    def test_ensure_directory_exists_create(self, mock_makedirs, mock_logger):
        directory = "/tmp/test_dir"
        with patch('os.path.exists', return_value=False):
            ensure_directory_exists(directory)
            mock_makedirs.assert_called_with(directory)
            mock_logger.info.assert_called_with(f"Created directory {directory}", emoji="✅")

    @patch('utils.logger')
    @patch('os.makedirs')
    def test_ensure_directory_exists_exists(self, mock_makedirs, mock_logger):
        directory = "/tmp/test_dir"
        with patch('os.path.exists', return_value=True):
            ensure_directory_exists(directory)
            mock_makedirs.assert_not_called()
            mock_logger.info.assert_called_with(f"Directory {directory} already exists", emoji="ℹ️")

    @patch('utils.logger')
    @patch('os.makedirs', side_effect=Exception("Error creating directory"))
    def test_ensure_directory_exists_error(self, mock_makedirs, mock_logger):
        directory = "/tmp/test_dir"
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(Exception) as context:
                ensure_directory_exists(directory)
            self.assertEqual(str(context.exception), "Error creating directory")
            mock_logger.error.assert_called_with(f"Error creating directory {directory}: Error creating directory",
                                                 emoji="❌")


if __name__ == '__main__':
    unittest.main()
