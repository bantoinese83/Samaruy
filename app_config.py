from typing import Dict, Set, List

import matchering as mg

# Constants for configuration
STEM_OPTIONS: Dict[int, str] = {2: 'spleeter:2stems', 4: 'spleeter:4stems', 5: 'spleeter:5stems'}
LOCAL_DIR: str = 'Stems'
ALLOWED_EXTENSIONS: Set[str] = {'.mp3', '.wav'}
MAX_FILE_SIZE_MB: int = 50

# Constants for file paths and result options
TARGET_AUDIO_PATH: str = "test/test.mp3"
REFERENCE_AUDIO_PATH: str = "reference_audio/rock_reference.mp3"
RESULTS: List[mg.Result] = [mg.pcm16("results/mastered_output_16bit.wav"),
                            mg.pcm24("results/mastered_output_24bit.wav"), ]

# Preset references for popular music genres
GENRE_REFERENCES: Dict[str, str] = {
    "rock": "reference_audio/rock_reference.mp3",
    "pop": "reference_audio/pop_reference.mp3",
    "jazz": "reference_audio/jazz_reference.mp3",
    "classical": "reference_audio/classical_reference.mp3",
    "hiphop": "reference_audio/hiphop_reference.mp3",
    "edm": "reference_audio/edm_reference.mp3",
    "country": "reference_audio/country_reference.mp3",
    "metal": "reference_audio/metal_reference.mp3",
    "blues": "reference_audio/blues_reference.mp3",
    "reggae": "reference_audio/reggae_reference.mp3",
    "rnb": "reference_audio/rnb_reference.mp3",
    "soul": "reference_audio/soul_reference.mp3",
    "funk": "reference_audio/funk_reference.mp3",
    "disco": "reference_audio/disco_reference.mp3",
    "techno": "reference_audio/techno_reference.mp3",
    "house": "reference_audio/house_reference.mp3",
    "trance": "reference_audio/trance_reference.mp3",
    "dubstep": "reference_audio/dubstep_reference.mp3",
    "trap": "reference_audio/trap_reference.mp3",
    "reggaeton": "reference_audio/reggaeton_reference.mp3",
    "latin": "reference_audio/latin_reference.mp3",
    "kpop": "reference_audio/kpop_reference.mp3",
    "jpop": "reference_audio/jpop_reference.mp3",
    "indie": "reference_audio/indie_reference.mp3",
    "folk": "reference_audio/folk_reference.mp3",
    "ambient": "reference_audio/ambient_reference.mp3",
    "chill": "reference_audio/chill_reference.mp3",
    "lofi": "reference_audio/lofi_reference.mp3",
    "acoustic": "reference_audio/acoustic_reference.mp3",
    "regional": "reference_audio/regional_reference.mp3",
    "world": "reference_audio/world_reference.mp3",
    "other": "reference_audio/other_reference.mp3",
    "custom": "reference_audio/custom_reference.mp3",
}
