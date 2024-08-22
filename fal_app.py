import datetime
from pathlib import Path
import threading
from audiocraft.data.audio import audio_write
import fal
from fastapi import Response, status
import torch

DATA_DIR = Path("/data/audio")

PROMPTS = [
    "Create a futuristic lo-fi beat that blends modern electronic elements with synthwave influences. Incorporate smooth, atmospheric synths and gentle, relaxing rhythms to evoke a sense of a serene, neon-lit future. Ensure  the track is continuous with no background noise or interruptions, maintaining a calm and tranquil atmosphere throughout while adding a touch of retro-futuristic vibes.",
    "gentle lo-fi beat with a smooth, mellow piano melody in the background. Ensure there are no background noises or interruptions, maintaining a continuous and seamless flow throughout the track. The beat should be relaxing and tranquil, perfect for a calm and reflective atmosphere.",
    "Create an earthy lo-fi beat that evokes a natural, grounded atmosphere. Incorporate organic sounds like soft percussion, rustling leaves, and gentle acoustic instruments. The track should have a warm, soothing rhythm with a continuous flow and no background noise or interruptions, maintaining a calm and reflective ambiance throughout.",
    "Create a soothing lo-fi beat featuring gentle, melodic guitar riffs. The guitar should be the focal point, supported by subtle, ambient electronic elements and a smooth, relaxed rhythm. Ensure the track is continuous with no background noise or interruptions, maintaining a warm and mellow atmosphere throughout.",
    "Create an ambient lo-fi beat with a tranquil and ethereal atmosphere. Use soft, atmospheric pads, gentle melodies, and minimalistic percussion to evoke a sense of calm and serenity. Ensure the track is continuous with no background noise or interruptions, maintaining a soothing and immersive ambiance throughout.",
]


class InfinifiFalApp(fal.App, keep_alive=300):
    machine_type = "GPU-A6000"
    requirements = [
        "torch==2.1.0",
        "audiocraft==1.3.0",
        "torchaudio==2.1.0",
        "websockets==11.0.3",
        "numpy==1.26.4",
    ]

    __is_generating = False

    def setup(self):
        import torchaudio
        from audiocraft.models.musicgen import MusicGen

        self.model = MusicGen.get_pretrained("facebook/musicgen-large")
        self.model.set_generation_params(duration=60)

    @fal.endpoint("/generate")
    def run(self):
        if self.__is_generating:
            return Response(status_code=status.HTTP_409_CONFLICT)
        threading.Thread(target=self.__generate_audio).start()

    @fal.endpoint("/clips/{index}")
    def get_clips(self, index):
        if self.__is_generating:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        path = DATA_DIR.joinpath(f"{index}")
        with open(path.with_suffix(".mp3"), "rb") as f:
            data = f.read()
            return Response(content=data)

    def __generate_audio(self):
        self.__is_generating = True

        print(f"[INFO] {datetime.datetime.now()}: generating audio...")

        wav = self.model.generate(PROMPTS)
        for i, one_wav in enumerate(wav):
            path = DATA_DIR.joinpath(f"{i}")
            audio_write(
                path,
                one_wav.cpu(),
                self.model.sample_rate,
                format="mp3",
                strategy="loudness",
                loudness_compressor=True,
                make_parent_dir=True,
            )

        self.__is_generating = False
