import threading
import os
from time import sleep
import requests

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from logger import log_info, log_warn
from websocket_connection_manager import WebSocketConnectionManager

# the index of the current audio track from 0 to 9
current_index = -1
# the timer that periodically advances the current audio track
t = None
inference_url = ""
ws_connection_manager = WebSocketConnectionManager()
active_listeners = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ws, inference_url

    inference_url = os.environ.get("INFERENCE_SERVER_URL")
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
        print(f"{inference_url}/generate")
        requests.post(f"{inference_url}/generate")
    except:
        log_warn(
            "inference server potentially unreachable. recycling cached audio for now."
        )
        return

    is_available = False
    while not is_available:
        try:
            res = requests.post(f"{inference_url}/clips/0", stream=True)
        except:
            log_warn(
                "inference server potentially unreachable. recycling cached audio for now."
            )
            return

        if res.status_code != status.HTTP_200_OK:
            print("still generating...")
            sleep(5)
            continue

        print("inference complete! downloading new clips")

        is_available = True
        with open(f"{offset}.mp3", "wb") as f:
            for chunk in res.iter_content(chunk_size=128):
                f.write(chunk)

    for i in range(4):
        res = requests.post(f"{inference_url}/clips/{i + 1}", stream=True)

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

    await ws_connection_manager.broadcast(f"{len(active_listeners)}")

    try:
        while True:
            msg = await ws.receive_text()

            if msg == "playing":
                active_listeners.add(addr)
                await ws_connection_manager.broadcast(f"{len(active_listeners)}")
            elif msg == "paused":
                active_listeners.discard(addr)
                await ws_connection_manager.broadcast(f"{len(active_listeners)}")

    except WebSocketDisconnect:
        active_listeners.discard(addr)
        ws_connection_manager.disconnect(ws)
        await ws_connection_manager.broadcast(f"{len(active_listeners)}")


app.mount("/", StaticFiles(directory="web", html=True), name="web")
