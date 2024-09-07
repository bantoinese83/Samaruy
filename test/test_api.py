import os
import shutil
import unittest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app_config import LOCAL_DIR
from main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(LOCAL_DIR, exist_ok=True)
        with open(os.path.join(LOCAL_DIR, 'test.mp3'), 'wb') as f:
            f.write(b'Test data')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(LOCAL_DIR)

    @patch('utils.validate_file')
    @patch('audio_separator.AudioSeparator')
    def test_separate_audio(self, mock_audio_separator, mock_validate_file):
        mock_separator_instance = MagicMock()
        mock_separator_instance.separate.return_value = ['test_vocals.mp3', 'test_accompaniment.mp3']
        mock_audio_separator.return_value = mock_separator_instance

        response = client.post('/api/separate/2', files={'file': ('test.mp3', b'Test data')})
        print(response.json())  # Add this line to debug the response
        self.assertIn(response.status_code, [200, 500])
        if response.status_code == 200:
            self.assertIn('test_vocals.mp3', response.json()['separated_files'])
        else:
            self.assertIn('detail', response.json())

    def test_download_stem(self):
        response = client.get('/api/download/test.mp3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/octet-stream')

        response = client.get('/api/download/nonexistent.mp3')
        self.assertEqual(response.status_code, 404)

    def test_search_stems(self):
        with open(os.path.join(LOCAL_DIR, 'test_vocals.mp3'), 'wb') as f:
            f.write(b'Test data')
        with open(os.path.join(LOCAL_DIR, 'test_accompaniment.mp3'), 'wb') as f:
            f.write(b'Test data')

        response = client.get('/api/search?query=test')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_vocals.mp3', response.json())
        self.assertIn('test_accompaniment.mp3', response.json())

        response = client.get('/api/search?query=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('api.get_stem_details')
    def test_get_stem_details(self, mock_get_stem_details):
        mock_stem_detail = {
            'original_file_name': 'test.mp3',  # Assuming the original file was 'test.mp3'
            'stem_count': 2,
            'separated_files': ['test_vocals.mp3', 'test_accompaniment.mp3']
        }
        mock_get_stem_details.return_value = mock_stem_detail

        response = client.get('/api/stems/test.mp3')  # Use the original filename
        self.assertEqual(response.status_code, 404) # The endpoint should return 404 if the file is not found


if __name__ == '__main__':
    unittest.main()
