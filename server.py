import threading
import os
from time import sleep
import requests

from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    WebSocket,
    status,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from listener_counter import ListenerCounter
from logger import log_info, log_warn
from websocket_connection_manager import WebSocketConnectionManager

# the index of the current audio track from 0 to 9
current_index = -1
# the timer that periodically advances the current audio track
t = None
inference_url = ""
api_key = ""
ws_connection_manager = WebSocketConnectionManager()
listener_counter = ListenerCounter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ws, inference_url, api_key

    inference_url = os.environ.get("INFERENCE_SERVER_URL")
    api_key = os.environ.get("API_KEY")

    if not inference_url:
        inference_url = "http://localhost:8001"

    advance()

    yield

    if t:
        t.cancel()


def generate_new_audio():
    if not inference_url:
        return

    global current_index

    offset = 0
    if current_index == 0:
        offset = 5
    elif current_index == 5:
        offset = 0
    else:
        return

    log_info("requesting new audio...")

    try:
        requests.post(
            f"{inference_url}/generate",
            headers={"Authorization": f"key {api_key}"},
        )
    except:
        log_warn(
            "inference server potentially unreachable. recycling cached audio for now."
        )
        return

    is_available = False
    while not is_available:
        try:
            res = requests.post(
                f"{inference_url}/clips/0",
                stream=True,
                headers={"Authorization": f"key {api_key}"},
            )
        except:
            log_warn(
                "inference server potentially unreachable. recycling cached audio for now."
            )
            return

        if res.status_code != status.HTTP_200_OK:
            print(res.status_code)
            print("still generating...")
            sleep(30)
            continue

        print("inference complete! downloading new clips")

        is_available = True
        with open(f"{offset}.mp3", "wb") as f:
            for chunk in res.iter_content(chunk_size=128):
                f.write(chunk)

    for i in range(4):
        res = requests.post(
            f"{inference_url}/clips/{i + 1}",
            stream=True,
            headers={"Authorization": f"key {api_key}"},
        )

        if res.status_code != status.HTTP_200_OK:
            continue

        with open(f"{i + 1 + offset}.mp3", "wb") as f:
            for chunk in res.iter_content(chunk_size=128):
                f.write(chunk)

    log_info("audio generated.")


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
    return FileResponse(f"{current_index}.mp3")


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws_connection_manager.connect(ws)

    addr = ""
    if ws.client:
        addr, _ = ws.client
    else:
        await ws.close()
        ws_connection_manager.disconnect(ws)
        return

    await ws_connection_manager.broadcast(f"{listener_counter.count()}")

    try:
        while True:
            msg = await ws.receive_text()
            match msg:
                case "listening":
                    listener_counter.add_listener(addr)
                    await ws_connection_manager.broadcast(f"{listener_counter.count()}")
                case "paused":
                    listener_counter.remove_listener(addr)
                    await ws_connection_manager.broadcast(f"{listener_counter.count()}")
    except:
        listener_counter.remove_listener(addr)
        ws_connection_manager.disconnect(ws)
        await ws_connection_manager.broadcast(f"{listener_counter.count()}")


app.mount("/", StaticFiles(directory="web", html=True), name="web")
