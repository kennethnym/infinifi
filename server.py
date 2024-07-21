import threading
import io

import torch
import modal
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from audiocraft.data.audio import audio_write

# the index of the current audio track from 0 to 9
current_index = -1
# the timer that periodically advances the current audio track
t = None

prompts = [
    "gentle, calming lo-fi beats that helps with studying and focusing",
    "calm, piano lo-fi beats to help with studying and focusing",
    "gentle lo-fi hip-hop to relax to",
    "gentle, quiet synthwave lo-fi beats",
    "morning lo-fi beats",
]


model = modal.Cls.lookup("infinifi", "Model")


@asynccontextmanager
async def lifespan(app: FastAPI):
    advance()
    yield
    if t:
        t.cancel()


def generate_new_audio():
    global current_index

    offset = 0
    wav_buf = None
    if current_index == 0:
        offset = 5
        wav_buf = model.generate.remote(prompts)
    elif current_index == 5:
        offset = 0
        wav_buf = model.generate.remote(prompts)
    else:
        return

    wav = torch.load(io.BytesIO(wav_buf), map_location=torch.device("cpu"))
    sample_rate = model.sample_rate.remote()

    print("generating new audio...")

    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(
            f"{idx + offset}",
            one_wav.cpu(),
            sample_rate,
            format="mp3",
            strategy="loudness",
            loudness_compressor=True,
        )

    print("audio generated.")


def advance():
    global current_index, t

    if current_index == 9:
        current_index = 0
    else:
        current_index = current_index + 1

    threading.Thread(target=generate_new_audio).start()

    t = threading.Timer(60, advance)
    t.start()


app = FastAPI(lifespan=lifespan)


@app.get("/current.mp3")
def get_current_audio():
    print("hello")
    return FileResponse(f"{current_index}.mp3")


app.mount("/", StaticFiles(directory="web", html=True), name="web")
