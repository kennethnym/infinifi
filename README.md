# infinifi

infinifi is a cosy little website that plays calm, gentle lo-fi music in the background to help you relax and study!

## audio generation

infinifi works by continuously generating 5 1-minute lofi music clips in the background using Meta's [MusicGen](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md) model. Each clip is generated using a slightly different prompt to provide music clips with different, but still cosy vibes.

## frontend

the frontend is written using pure HTML/CSS/JS with no external dependencies. it queries `/current.mp3` to obtain the current lofi music clip. after the clip ends, it re-queries again, which will return a different clip. since each clip is completely different, the frontend applies a fade-in and fade-out effect at the start and the end of each clip.

## feature requests

if you have any feature idea, feel free to use the issue tracker to let me know!

