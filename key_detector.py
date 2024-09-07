import os
import struct
import wave

import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

from logging_config import logger


def load_audio_file(file_path):
    try:
        if file_path.lower().endswith('.wav'):
            audio_file = wave.open(file_path, 'rb')
            file_length = audio_file.getnframes()
            f_s = audio_file.getframerate()
            sound = np.zeros(file_length)

            for i in range(file_length):
                wdata = audio_file.readframes(1)
                data = struct.unpack("<h", wdata)
                sound[i] = int(data[0])

            sound = np.divide(sound, float(2 ** 15))  # scaling it to 0-1
            return sound, f_s, audio_file.getnchannels()
        elif file_path.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(file_path)
            sound = np.array(audio.get_array_of_samples())
            f_s = audio.frame_rate
            sound = np.divide(sound, float(2 ** 15))  # scaling it to 0-1
            return sound, f_s, audio.channels
        else:
            raise ValueError("Unsupported file format. Only WAV and MP3 files are supported.")
    except Exception as e:
        logger.error(f"Error loading audio file: {e}", emoji="❌")
        raise


def save_waveform_plot(sound, title="Waveform", filename="waveform.png"):
    plt.plot(sound)
    plt.title(title)
    plt.savefig(filename)
    plt.close()


def perform_fft(sound):
    fourier = np.fft.fft(sound)
    fourier = np.absolute(fourier)
    return fourier


def detect_peak(fourier, f_s, file_length, counter):
    imax = np.argmax(fourier[0:int(file_length / 2)])
    threshold = 0.3 * fourier[imax]
    i_begin = -1
    i_end = -1  # Initialize i_end to avoid referencing before assignment

    for i in range(0, imax + 100):
        if fourier[i] >= threshold:
            if i_begin == -1:
                i_begin = i
        if i_begin != -1 and fourier[i] < threshold:
            i_end = i
            break

    if i_end == -1:  # Ensure i_end is set
        i_end = imax + 100

    imax = np.argmax(fourier[0:i_end + 100])
    freq = (imax * f_s) / (file_length * counter)
    return freq


def find_note(freq):
    name = np.array(
        ["C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1",
         "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G2#", "A2",
         "A2#", "B2", "C3", "C3#", "D3", "D3#", "E3", "F3", "F3#", "G3", "G3#", "A3", "A3#", "B3", "C4", "C4#", "D4",
         "D4#", "E4", "F4", "F4#", "G4", "G4#", "A4", "A4#", "B4", "C5", "C5#", "D5", "D5#", "E5", "F5", "F5#", "G5",
         "G5#", "A5", "A5#", "B5", "C6", "C6#", "D6", "D6#", "E6", "F6", "F6#", "G6", "G6#", "A6", "A6#", "B6", "C7",
         "C7#", "D7", "D7#", "E7", "F7", "F7#", "G7", "G7#", "A7", "A7#", "B7", "C8", "C8#", "D8", "D8#", "E8", "F8",
         "F8#", "G8", "G8#", "A8", "A8#", "B8", "Beyond B8"])
    frequencies = np.array(
        [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87, 32.70, 34.65, 36.71, 38.89,
         41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74, 65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00,
         103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00,
         233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
         523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50,
         1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53, 2093.00,
         2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07, 4186.01,
         4434.92, 4698.64, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040.00, 7458.62, 7902.13, 8000])

    for i in range(0, frequencies.size - 1):
        if freq < frequencies[0]:
            return name[0]
        if freq > frequencies[-1]:
            return name[-1]
        if frequencies[i] <= freq < frequencies[i + 1]:
            return name[i] if freq - frequencies[i] < (frequencies[i + 1] - frequencies[i]) / 2 else name[i + 1]
    return "Unknown"


def key_detect(file_path):
    sound, f_s, counter = load_audio_file(file_path)
    save_waveform_plot(sound, "Original Waveform", "img/original_waveform.png")
    fourier = perform_fft(sound)
    save_waveform_plot(fourier, "Fourier Transform", "img/fourier_transform.png")
    freq = detect_peak(fourier, f_s, len(sound), counter)
    note = find_note(freq)
    return note


if __name__ == "__main__":
    path = os.getcwd()
    file_name = os.path.join(path, "test/test.mp3"
                                   "")
    try:
        detected_note = key_detect(file_name)
        print(f"\n\tDetected Note = {detected_note}")
    except Exception as e:
        print(f"Error: {e}")
