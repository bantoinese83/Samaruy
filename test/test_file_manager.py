import unittest
from io import BytesIO
from unittest.mock import patch, mock_open

from file_manager import File_Manager


class TestFileManager(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b'Test data')
    def test_download_from_directory_success(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = File_Manager.download_from_directory('test.mp3', '/tmp')
        self.assertIsInstance(result, BytesIO)
        self.assertEqual(result.read(), b'Test data')

    @patch('os.path.exists')
    def test_download_from_directory_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            File_Manager.download_from_directory('test.mp3', '/tmp')

    @patch('os.path.exists')
    @patch('builtins.open', side_effect=IOError('Read error'))
    def test_download_from_directory_read_error(self, mock_file, mock_exists):
        mock_exists.return_value = True
        with self.assertRaises(IOError):
            File_Manager.download_from_directory('test.mp3', '/tmp')

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_directory_success(self, mock_file, mock_makedirs, mock_exists):
        mock_exists.side_effect = [False, True]
        file_data = BytesIO(b'Test data')
        File_Manager.save_to_directory(file_data, 'test.mp3', '/tmp')
        mock_makedirs.assert_called_once_with('/tmp')
        mock_file().write.assert_called_once_with(b'Test data')

    def test_save_to_directory_valid_file_data(self):
        valid_data = BytesIO(b"valid data")
        try:
            File_Manager.save_to_directory(valid_data, 'test.mp3', '/tmp')
        except ValueError:
            self.fail("save_to_directory() raised ValueError unexpectedly!")

    @patch('os.path.exists')
    @patch('builtins.open', side_effect=IOError('Write error'))
    def test_save_to_directory_write_error(self, mock_file, mock_exists):
        mock_exists.return_value = True
        file_data = BytesIO(b'Test data')
        with self.assertRaises(IOError):
            File_Manager.save_to_directory(file_data, 'test.mp3', '/tmp')

    @patch('os.path.exists')
    def test_cleanup_directory_no_directory(self, mock_exists):
        mock_exists.return_value = False
        File_Manager.cleanup_directory('/tmp', days_old=7)

    @patch('os.path.exists')
    @patch('os.remove')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')  # Add this line to mock os.path.isfile
    def test_cleanup_directory(self, mock_isfile, mock_getmtime, mock_listdir, mock_remove, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['old_file.mp3']
        mock_getmtime.return_value = 0  # Ensure file appears very old
        mock_isfile.return_value = True  # Ensure os.path.isfile returns True
        File_Manager.cleanup_directory('/tmp', days_old=7)
        mock_remove.assert_called_once_with('/tmp/old_file.mp3')

    @patch('os.path.exists')
    @patch('os.remove', side_effect=IOError('Delete error'))
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')  # Add this line to mock os.path.isfile
    def test_cleanup_directory_delete_error(self, mock_isfile, mock_getmtime, mock_listdir, mock_remove, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['old_file.mp3']
        mock_getmtime.return_value = 0  # Ensure file appears very old
        mock_isfile.return_value = True  # Ensure os.path.isfile returns True
        with self.assertRaises(IOError):  # Assert for IOError, not OSError
            File_Manager.cleanup_directory('/tmp', days_old=7)


if __name__ == '__main__':
    unittest.main()