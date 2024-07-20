const playBtn = document.getElementById("play-btn");

let isPlaying = false;
let currentAudio;
let volume = 1;

function playAudio() {
	currentAudio = new Audio("/current.mp3");
	currentAudio.onplay = () => {
		isPlaying = true;
		playBtn.innerText = "pause";
	};
	currentAudio.onpause = () => {
		isPlaying = false;
		playBtn.innerText = "play";
	};

	currentAudio.volume = volume;

	currentAudio.load();
	currentAudio.play();
}

function pauseAudio() {
	currentAudio.pause();
}

playBtn.onclick = () => {
	if (isPlaying) {
		pauseAudio();
	} else {
		playAudio();
	}
};
