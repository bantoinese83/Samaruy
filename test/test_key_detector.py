import struct
import unittest
from unittest.mock import patch, MagicMock

import numpy as np

from key_detector import load_audio_file, key_detect


class TestKeyDetector(unittest.TestCase):

    @patch('key_detector.wave.open')
    def test_load_wav_file(self, mock_wave_open):
        mock_wave = MagicMock()
        mock_wave.getnframes.return_value = 100
        mock_wave.getframerate.return_value = 44100
        mock_wave.readframes.return_value = struct.pack("<h", 1000)
        mock_wave_open.return_value = mock_wave

        sound, f_s, channels = load_audio_file('test.wav')
        self.assertEqual(f_s, 44100)
        self.assertEqual(channels, mock_wave.getnchannels())
        self.assertTrue(np.allclose(sound, np.array([1000] * 100) / float(2 ** 15)))

    @patch('key_detector.AudioSegment.from_mp3')
    def test_load_mp3_file(self, mock_from_mp3):
        mock_audio = MagicMock()
        mock_audio.get_array_of_samples.return_value = [1000] * 100
        mock_audio.frame_rate = 44100
        mock_audio.channels = 2
        mock_from_mp3.return_value = mock_audio

        sound, f_s, channels = load_audio_file('test.mp3')
        self.assertEqual(f_s, 44100)
        self.assertEqual(channels, 2)
        self.assertTrue(np.allclose(sound, np.array([1000] * 100) / float(2 ** 15)))

    def test_unsupported_file_format(self):
        with self.assertRaises(ValueError):
            load_audio_file('test.txt')

    @patch('key_detector.save_waveform_plot')
    @patch('key_detector.perform_fft')
    @patch('key_detector.detect_peak')
    @patch('key_detector.find_note')
    @patch('key_detector.load_audio_file')
    def test_note_detect(self, mock_load_audio_file, mock_find_note, mock_detect_peak, mock_perform_fft,
                         mock_save_waveform_plot):
        mock_load_audio_file.return_value = (np.array([0.1] * 100), 44100, 2)
        mock_perform_fft.return_value = np.array([0.1] * 100)
        mock_detect_peak.return_value = 440.0
        mock_find_note.return_value = "A4"

        note = key_detect('test.mp3')
        self.assertEqual(note, "A4")
        mock_save_waveform_plot.assert_called()
        mock_perform_fft.assert_called()
        mock_detect_peak.assert_called()
        mock_find_note.assert_called()


if __name__ == '__main__':
    unittest.main()
