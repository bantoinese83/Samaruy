import unittest
import warnings
from unittest.mock import patch

import numpy as np

from bpm_detector import detect_bpm


class TestBpmDetector(unittest.TestCase):

    @patch('librosa.load')
    def test_valid_mp3_file(self, mock_load):
        # Mock the return value of librosa.load for a valid MP3 file
        mock_load.return_value = (np.array([0.1] * 22050), 22050)
        tempo, beat_times = detect_bpm('test/test.mp3')
        self.assertIsInstance(tempo, int)
        self.assertIsInstance(beat_times, list)

    @patch('librosa.load')
    def test_valid_wav_file(self, mock_load):
        # Mock the return value of librosa.load for a valid WAV file
        mock_load.return_value = (np.array([0.1] * 22050), 22050)
        tempo, beat_times = detect_bpm('test/test.wav')
        self.assertIsInstance(tempo, int)
        self.assertIsInstance(beat_times, list)

    def test_unsupported_file_format(self):
        tempo, beat_times = detect_bpm('test/test.txt')
        self.assertEqual(tempo, 0)
        self.assertEqual(beat_times, [])

    @patch('librosa.load')
    def test_empty_audio_file(self, mock_load):
        # Mock the return value of librosa.load for an empty audio file
        mock_load.return_value = (np.array([]), 22050)
        tempo, beat_times = detect_bpm('test/empty.mp3')
        self.assertEqual(tempo, 0)
        self.assertEqual(beat_times, [])

    @patch('librosa.load')
    def test_short_audio_file(self, mock_load):
        # Mock the return value of librosa.load for a short audio file
        mock_load.return_value = (np.array([0.1] * 100), 22050)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="n_fft=2048 is too small for input signal of length=100")
            tempo, beat_times = detect_bpm('test/short.mp3')
        self.assertEqual(tempo, 0)
        self.assertEqual(beat_times, [])


if __name__ == '__main__':
    unittest.main()
