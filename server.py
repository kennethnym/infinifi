import threading
from .generate import generate
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
current_index = 0

app.mount("/", StaticFiles(directory="web", html=True), name="web")


def advance():
    global current_index

    # if current_index == 0:
    #   generate(offset=5)
    # elif current_index == 5:
    #   generate(offset=0)

    if current_index == 9:
        current_index = 0
    else:
        current_index = current_index + 1

    t = threading.Timer(60, advance)
    t.start()


advance()
