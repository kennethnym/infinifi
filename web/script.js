const playBtn = document.getElementById("play-btn");
const catImg = document.getElementsByClassName("cat")[0];
const volumeSlider = document.getElementById("volume-slider");
const currentVolumeLabel = document.getElementById("current-volume-label");
const clickAudio = new Audio("./audio/click.wav");
const clickReleaseAudio = new Audio("./audio/click-release.wav");

const CROSSFADE_DURATION_MS = 5000;
const CROSSFADE_INTERVAL_MS = 20;
const AUDIO_DURATION_MS = 60000;

let isPlaying = false;
let isFading = false;
let currentAudio;
let maxVolume = 100;
let currentVolume = 0;

function playAudio() {
	// add a random query parameter at the end to prevent browser caching
	currentAudio = new Audio(`./current.mp3?t=${Date.now()}`);
	currentAudio.onplay = () => {
		isPlaying = true;
		playBtn.innerText = "pause";
	};
	currentAudio.onpause = () => {
		isPlaying = false;
		currentVolume = 0;
		playBtn.innerText = "play";
	};
	currentAudio.onended = () => {
		currentVolume = 0;
		playAudio();
	};
	currentAudio.volume = 0;

	currentAudio.play();

	fadeIn();
	setTimeout(() => {
		fadeOut();
	}, AUDIO_DURATION_MS - CROSSFADE_DURATION_MS);
}

function pauseAudio() {
	currentAudio.pause();
	currentAudio.volume = 0;
	currentVolume = 0;
}

function fadeIn() {
	isFading = true;

	// volume ranges from 0 to 100, this determines by how much the volume number
	// should be incremented at every step of the fade in
	const volumeStep =
		maxVolume / (CROSSFADE_DURATION_MS / CROSSFADE_INTERVAL_MS);
	const handle = setInterval(() => {
		currentVolume += volumeStep;
		if (currentVolume >= maxVolume) {
			clearInterval(handle);
			currentVolume = maxVolume;
			isFading = false;
		} else {
			currentAudio.volume = currentVolume / 100;
		}
	}, CROSSFADE_INTERVAL_MS);
}

function fadeOut() {
	isFading = true;

	// volume ranges from 0 to 100, this determines by how much the volume number
	// should be decremented at every step of the fade out
	const volumeStep =
		maxVolume / (CROSSFADE_DURATION_MS / CROSSFADE_INTERVAL_MS);
	const handle = setInterval(() => {
		currentVolume -= volumeStep;
		if (currentVolume <= 0) {
			clearInterval(handle);
			currentVolume = 0;
			isFading = false;
		} else {
			currentAudio.volume = currentVolume / 100;
		}
	}, CROSSFADE_INTERVAL_MS);
}

function animateCat() {
	let current = 0;
	setInterval(() => {
		if (current === 3) {
			current = 0;
		} else {
			current += 1;
		}
		catImg.src = `./images/cat-${current}.png`;
	}, 500);
}

playBtn.onmousedown = () => {
	clickAudio.play();
	document.addEventListener(
		"mouseup",
		() => {
			clickReleaseAudio.play();
		},
		{ once: true },
	);
};

playBtn.onclick = () => {
	if (isPlaying) {
		pauseAudio();
	} else {
		playAudio();
	}
};

volumeSlider.oninput = () => {
	maxVolume = volumeSlider.value;
	currentVolumeLabel.textContent = `${maxVolume}%`;
	if (!isFading && currentAudio) {
		currentAudio.volume = maxVolume / 100;
		currentVolume = maxVolume;
	}
};

volumeSlider.value = 100;
animateCat();
