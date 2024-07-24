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
    "Create a futuristic lo-fi beat that blends modern electronic elements with synthwave influences. Incorporate smooth, atmospheric synths and gentle, relaxing rhythms to evoke a sense of a serene, neon-lit future. Ensure  the track is continuous with no background noise or interruptions, maintaining a calm and tranquil atmosphere throughout while adding a touch of retro-futuristic vibes.",
    "gentle lo-fi beat with a smooth, mellow piano melody in the background. Ensure there are no background noises or interruptions, maintaining a continuous and seamless flow throughout the track. The beat should be relaxing and tranquil, perfect for a calm and reflective atmosphere.",
    "Create an earthy lo-fi beat that evokes a natural, grounded atmosphere. Incorporate organic sounds like soft percussion, rustling leaves, and gentle acoustic instruments. The track should have a warm, soothing rhythm with a continuous flow and no background noise or interruptions, maintaining a calm and reflective ambiance throughout.",
    "Create a soothing lo-fi beat featuring gentle, melodic guitar riffs. The guitar should be the focal point, supported by subtle, ambient electronic elements and a smooth, relaxed rhythm. Ensure the track is continuous with no background noise or interruptions, maintaining a warm and mellow atmosphere throughout.",
    "Create an ambient lo-fi beat with a tranquil and ethereal atmosphere. Use soft, atmospheric pads, gentle melodies, and minimalistic percussion to evoke a sense of calm and serenity. Ensure the track is continuous with no background noise or interruptions, maintaining a soothing and immersive ambiance throughout.",
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
