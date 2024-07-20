import threading

# from generate import generate
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
current_index = -1


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

    print(f"advancing, current index {current_index}")

    t = threading.Timer(60, advance)
    t.start()


advance()


@app.get("/current.mp3")
def get_current_audio():
    print("hello")
    return FileResponse(f"{current_index}.mp3")


app.mount("/", StaticFiles(directory="web", html=True), name="web")
