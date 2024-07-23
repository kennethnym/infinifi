# infinifi

infinifi is a cosy little website that plays calm, gentle lo-fi music in the background to help you relax and study!

## audio generation

infinifi works by continuously generating 5 1-minute lofi music clips in the background using Meta's [MusicGen](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md) model. Each clip is generated using a slightly different prompt to provide music clips with different, but still cosy vibes.

## frontend

the frontend is written using pure HTML/CSS/JS with no external dependencies. it queries `/current.mp3` to obtain the current lofi music clip. after the clip ends, it re-queries again, which will return a different clip. since each clip is completely different, the frontend applies a fade-in and fade-out effect at the start and the end of each clip.

## inference

infinifi consists of two parts, the inference server and the web server. the two servers are connected via a websocket connection. whenever the web server requires new audio clips to be generated, it sends a "generate" message to the inference server, which triggers the generation on the inference server. when the generation is done, the inference server sends back the audio in mp3 format back to the web server over websocket. once the web server receives the mp3 data, it saves them locally as mp3 files.

## running it yourself

you are welcome to self host infinifi. to get started, make sure that: 

- you are using python 3.9/3.10;
- port 8001 (used by the inference server) is free.

then follow the steps below:

1. install `torch==2.1.0`
2. install deps from both `requirements-inference.txt` and `requirements-server.txt`
3. run the inference server: `python inference_server.py`
4. run the web server: `fastapi run server.py --port ${ANY_PORT_NUMBER}`

you can also run the inference server and the web server on separate machines. to let the web server know where to connect to the inference server, specify the `INFERENCE_SERVER_WS_URL` environment variable when running the web server:

```
INFERENCE_SERVER_WS_URL=ws://2.3.1.4:1938 fastapi run server.py --port ${ANY_PORT_NUMBER}
```

## feature requests

if you have any feature idea, feel free to use the issue tracker to let me know!

