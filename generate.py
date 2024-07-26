import torchaudio
from audiocraft.models.musicgen import MusicGen
from audiocraft.data.audio import audio_write

from prompts import PROMPTS

MODEL_NAME = "facebook/musicgen-large"
MUSIC_DURATION_SECONDS = 60

model = MusicGen.get_pretrained(MODEL_NAME)
model.set_generation_params(duration=MUSIC_DURATION_SECONDS)


def generate(offset=0):
    wav = model.generate(PROMPTS)

    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(
            f"{idx + offset}",
            one_wav.cpu(),
            model.sample_rate,
            format="mp3",
            strategy="loudness",
            loudness_compressor=True,
        )
