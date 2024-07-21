from audiocraft.models.musicgen import MusicGen
import modal
import io
import torch


MODEL_DIR = "/root/model/model_input"
MODEL_ID = "facebook/musicgen-large"
N_GPUS = 1
GPU_CONFIG = modal.gpu.A100(count=N_GPUS)


def download_model():
    import torchaudio
    from audiocraft.models.musicgen import MusicGen

    MusicGen.get_pretrained(MODEL_ID)


image = modal.Image.from_registry("python:3.9.19-slim-bookworm")

image = (
    image.apt_install("ffmpeg")
    .env({"AUDIOCRAFT_CACHE_DIR": MODEL_DIR})
    .pip_install("audiocraft==1.3.0", "torchaudio==2.1.0")
    .run_function(download_model, timeout=20 * 60)
)


app = modal.App("infinifi", image=image)


@app.cls(gpu=GPU_CONFIG, container_idle_timeout=15 * 60)
class Model:
    @modal.enter()
    def load(self):
        self.model = MusicGen.get_pretrained(MODEL_ID)
        self.model.set_generation_params(duration=60)

    @modal.method()
    def sample_rate(self):
        return self.model.sample_rate

    @modal.method()
    def generate(self, prompts):
        wav = self.model.generate(prompts)
        buf = io.BytesIO()
        torch.save(wav, buf)
        return buf.getvalue()
