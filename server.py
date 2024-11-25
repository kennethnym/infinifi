import asyncio
import threading
import os
import json
from time import sleep
import requests

from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from logger import log_info, log_warn
from websocket_connection_manager import WebSocketConnectionManager
from sse_starlette.sse import EventSourceResponse

# the index of the current audio track from 0 to 9
current_index = -1
# the timer that periodically advances the current audio track
t = None
inference_url = ""
api_key = ""
ws_connection_manager = WebSocketConnectionManager()
active_listeners = set()


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


@app.get("/status")
def status_stream(request: Request):
    async def status_generator():
        last_listener_count = len(active_listeners)
        yield json.dumps({"listeners": last_listener_count})

        while True:
            if await request.is_disconnected():
                break

            listener_count = len(active_listeners)
            if listener_count != last_listener_count:
                last_listener_count = listener_count
                yield json.dumps({"listeners": listener_count})

            await asyncio.sleep(1)

    return EventSourceResponse(status_generator())


@app.post("/client-status")
async def change_status(request: Request):
    body = await request.json()

    try:
        is_listening = body["isListening"]

        client = request.client
        if not client:
            raise HTTPException(status_code=400, detail="ip address unavailable.")

        if is_listening:
            active_listeners.add(client.host)
        else:
            active_listeners.discard(client.host)

        return {"isListening": is_listening}

    except KeyError:
        raise HTTPException(status_code=400, detail="'isListening' must be a boolean")


app.mount("/", StaticFiles(directory="web", html=True), name="web")
