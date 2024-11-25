# infinifi

infinifi is a cosy little website that plays calm, gentle lo-fi music in the background to help you relax and study!

## audio generation

infinifi works by continuously generating 5 1-minute lofi music clips in the background using Meta's [MusicGen](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md) model. Each clip is generated using a slightly different prompt to provide music clips with different, but still cosy vibes.

## frontend

the frontend is written using pure HTML/CSS/JS with no external dependencies. it queries `/current.mp3` to obtain the current lofi music clip. after the clip ends, it re-queries again, which will return a different clip. since each clip is completely different, the frontend applies a fade-in and fade-out effect at the start and the end of each clip.

## inference

infinifi consists of two parts, the inference server and the web server. 5 audio clips are generated each time an inference request is received from the web server. the web server will request for an inference every set interval. after the request is made, it polls the inference server until the audio is generated and available for download. it then downloads the 5 generated clips and saves it locally. at most 10 clips are saved at a time.

when the inference server is down, the web server will recycle saved clips until it is back up again.

## requirements

- python >= 3.10 (tested with python 3.12 only)

## running it yourself

i have recently changed the networking between the web server and the inference server. at the moment, the inference happens on fal infrastructure (`fal_app.py`), and i have yet to update the standalone inference server code `inference_server.py` to match the new architecture.

## feature requests

if you have any feature idea, feel free to use the issue tracker to let me know!

## credits:

- cats by [@PixElthen](https://x.com/pixelthen)

