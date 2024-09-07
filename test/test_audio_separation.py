# test/test_audio_separation.py

import os
import shutil
import unittest
from unittest.mock import patch

import numpy as np

from audio_separator import AudioSeparator


class TestAudioSeparation(unittest.TestCase):

    def setUp(self):
        os.makedirs('/tmp/output', exist_ok=True)
        with open('/tmp/output/file1.mp3', 'wb') as f:
            f.write(b'Test data')

    def tearDown(self):
        shutil.rmtree('/tmp/output')

    @patch('librosa.load')
    def test_detect_bpm(self, mock_load):
        mock_load.return_value = (np.array([0.1] * 22050), 22050)
        result = AudioSeparator.detect_bpm('test.mp3')
        self.assertIsInstance(result, int)

    @patch('key_detector.load_audio_file')
    @patch('key_detector.key_detect')
    @patch('audio_separator.key_detect')
    def test_detect_key(self, mock_key_detect, mock_key_detect_audio_separator, mock_load_audio_file):
        mock_key_detect.return_value = "A4"
        result = AudioSeparator.detect_key('test.mp3')
        self.assertEqual(result, "A4")

    def test_collect_separated_files(self):
        result = AudioSeparator.collect_separated_files('/tmp/output')
        self.assertIn('file1.mp3', result)


if __name__ == '__main__':
    unittest.main()
