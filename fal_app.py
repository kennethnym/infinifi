import io
import fal
from fastapi import WebSocket
import torch
from fal.toolkit import File

from prompts import PROMPTS


class InfinifiFalApp(fal.App, keep_alive=300):
    machine_type = "GPU-A6000"
    requirements = [
        "torch==2.1.0",
        "audiocraft==1.3.0",
        "torchaudio==2.1.0",
        "websockets==11.0.3",
    ]

    def setup(self):
        import torchaudio
        from audiocraft.models.musicgen import MusicGen

        self.model = MusicGen.get_pretrained("facebook/musicgen-large")
        self.model.set_generation_params(duration=60)

    @fal.endpoint("/generate")
    def run(self):
        wav = self.model.generate(PROMPTS)

        serialized = []
        for one_wav in wav:
            buf = io.BytesIO()
            torch.save(one_wav.cpu(), buf)
            serialized.append(buf.getvalue())

        return serialized

    @fal.endpoint("/ws")
    async def run_ws(self, ws: WebSocket):
        await ws.accept()

        wav = self.model.generate(PROMPTS)

        for one_wav in enumerate(wav):
            buf = io.BytesIO()
            torch.save(one_wav, buf)
            await ws.send_bytes(buf.getvalue())

        await ws.close()
