import torchaudio
import time
from audiocraft.models.musicgen import MusicGen
from audiocraft.data.audio import audio_write

MODEL_NAME = "facebook/musicgen-large"
MUSIC_DURATION_SECONDS = 60

print("obtaining model...")

model = MusicGen.get_pretrained(MODEL_NAME)
model.set_generation_params(duration=MUSIC_DURATION_SECONDS)
descriptions = [
    "gentle, calming lo-fi beats that helps with studying and focusing",
    "calm, piano lo-fi beats to help with studying and focusing",
    "gentle lo-fi hip-hop to relax to",
    "gentle, quiet synthwave lo-fi beats",
    "morning lo-fi beats",
]

print("model obtained. generating audio...")

a = time.time()
wav = model.generate(descriptions)
b = time.time()

print(f"audio generated. took {b - a} seconds.")

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(
        f"{idx}",
        one_wav.cpu(),
        model.sample_rate,
        format="mp3",
        strategy="loudness",
        loudness_compressor=True,
    )
