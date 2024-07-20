const playBtn = document.getElementById("play-btn");

const CROSSFADE_DURATION_MS = 5000;
const CROSSFADE_INTERVAL_MS = 20;
const AUDIO_DURATION_MS = 60000;

let isPlaying = false;
let currentAudio;
let volume = 0;

function playAudio() {
	// add a random query parameter at the end to prevent browser caching
	currentAudio = new Audio(`/current.mp3?t=${Date.now()}`);
	currentAudio.onplay = () => {
		isPlaying = true;
		playBtn.innerText = "pause";
	};
	currentAudio.onpause = () => {
		isPlaying = false;
		playBtn.innerText = "play";
	};
	currentAudio.volume = volume;

	currentAudio.play();

	fadeIn();
	setTimeout(() => {
		fadeOut();
	}, AUDIO_DURATION_MS - CROSSFADE_DURATION_MS);
}

function pauseAudio() {
	currentAudio.pause();
}

function fadeIn() {
	// volume ranges from 0 to 100, this determines by how much the volume number
	// should be incremented at every step of the fade in
	const volumeStep = 100 / (CROSSFADE_DURATION_MS / CROSSFADE_INTERVAL_MS);
	const handle = setInterval(() => {
		volume += volumeStep;
		if (volume >= 100) {
			clearInterval(handle);
		} else {
			currentAudio.volume = volume / 100;
		}
	}, CROSSFADE_INTERVAL_MS);
}

function fadeOut() {
	// volume ranges from 0 to 100, this determines by how much the volume number
	// should be decremented at every step of the fade out
	const volumeStep = 100 / (CROSSFADE_DURATION_MS / CROSSFADE_INTERVAL_MS);
	const handle = setInterval(() => {
		volume -= volumeStep;
		if (volume <= 0) {
			clearInterval(handle);
		} else {
			currentAudio.volume = volume / 100;
		}
	}, CROSSFADE_INTERVAL_MS);
}

playBtn.onclick = () => {
	if (isPlaying) {
		pauseAudio();
	} else {
		playAudio();
	}
};
