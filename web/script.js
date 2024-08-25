const CROSSFADE_DURATION_MS = 5000;
const CROSSFADE_INTERVAL_MS = 20;
const AUDIO_DURATION_MS = 60000;
const SAVE_VOLUME_TIMEOUT_MS = 200;

const ACHIEVEMENT_A_LITTLE_CHATTY = "a-little-chatty";

const playBtn = document.getElementById("play-btn");
const catImg = document.getElementById("cat");
const heartImg = document.getElementById("heart");
const volumeSlider = document.getElementById("volume-slider");
const currentVolumeLabel = document.getElementById("current-volume-label");
const listenerCountLabel = document.getElementById("listener-count");
const notificationContainer = document.getElementById("notification");
const notificationTitle = document.getElementById("notification-title");
const notificationBody = document.getElementById("notification-body");

const clickAudio = document.getElementById("click-audio");
const clickReleaseAudio = document.getElementById("click-release-audio");
const meowAudio = document.getElementById("meow-audio");
const achievementUnlockedAudio = document.getElementById(
	"achievement-unlocked-audio",
);

let isPlaying = false;
let isFading = false;
let currentAudio;
let maxVolume = 100;
let currentVolume = 0;
let saveVolumeTimeout = null;
let meowCount = 0;
let ws = connectToWebSocket();

function playAudio() {
	// add a random query parameter at the end to prevent browser caching
	currentAudio = new Audio(`./current.mp3?t=${Date.now()}`);
	currentAudio.onplay = () => {
		isPlaying = true;
		playBtn.innerText = "pause";
		if (ws) {
			ws.send("playing");
		}
	};
	currentAudio.onpause = () => {
		isPlaying = false;
		currentVolume = 0;
		playBtn.innerText = "play";
		if (ws) {
			ws.send("paused");
		}
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

/**
 * Allow audio to be played/paused using the space bar
 */
function enableSpaceBarControl() {
	document.addEventListener("keydown", (event) => {
		if (event.code === "Space") {
			playBtn.classList.add("button-active");
			playBtn.dispatchEvent(new MouseEvent("mousedown"));
			clickAudio.play();
		}
	});
	document.addEventListener("keyup", (event) => {
		if (event.code === "Space") {
			playBtn.classList.remove("button-active");
			clickReleaseAudio.play();
		}
	});
	document.addEventListener("keypress", (event) => {
		if (event.code === "Space") {
			playBtn.click();
		}
	});
}

function connectToWebSocket() {
	const ws = new WebSocket(
		`${location.protocol === "https:" ? "wss:" : "ws:"}//${location.host}/ws`,
	);
	ws.onmessage = (event) => {
		console.log(event.data);

		if (typeof event.data !== "string") {
			return;
		}

		const listenerCountStr = event.data;
		const listenerCount = Number.parseInt(listenerCountStr);
		if (Number.isNaN(listenerCount)) {
			return;
		}

		if (listenerCount <= 1) {
			listenerCountLabel.innerText = `${listenerCount} person tuned in`;
		} else {
			listenerCountLabel.innerText = `${listenerCount} ppl tuned in`;
		}
	};

	return ws;
}

function changeVolume(volume) {
	maxVolume = volume;
	const v = maxVolume / 100;

	currentVolumeLabel.textContent = `${maxVolume}%`;

	if (!isFading && currentAudio) {
		currentAudio.volume = v;
		currentVolume = maxVolume;
	}

	clickAudio.volume = v;
	clickReleaseAudio.volume = v;
	meowAudio.volume = v;
}

function loadInitialVolume() {
	const savedVolume = localStorage.getItem("volume");
	let volume = 100;
	if (savedVolume) {
		volume = Number.parseInt(savedVolume);
		if (Number.isNaN(volume)) {
			volume = 100;
		}
	}
	volumeSlider.value = volume;
	changeVolume(volume);

	document.getElementById("volume-slider-container").style.display = "flex";
}

function loadMeowCount() {
	const lastMeowCount = localStorage.getItem("meowCount");
	if (!lastMeowCount) {
		meowCount = 0;
	} else {
		const n = Number.parseInt(lastMeowCount);
		if (Number.isNaN(n)) {
			meowCount = 0;
		} else {
			meowCount += n;
		}
	}
}

function showNotification(title, content, duration) {
	notificationTitle.innerText = title;
	notificationBody.innerText = content;
	notificationContainer.style.display = "block";
	notificationContainer.style.animation = "0.5s linear 0s notification-fade-in";
	setTimeout(() => {
		notificationContainer.style.animation =
			"0.5s linear 0s notification-fade-out";
		setTimeout(() => {
			notificationContainer.style.display = "none";
		}, 450);
	}, duration);
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

catImg.onmousedown = () => {
	meowAudio.play();
};

playBtn.onclick = () => {
	if (isPlaying) {
		pauseAudio();
	} else {
		playAudio();
	}
};

volumeSlider.oninput = () => {
	const volume = volumeSlider.value;
	changeVolume(volume);
	if (saveVolumeTimeout) {
		clearTimeout(saveVolumeTimeout);
	}
	saveVolumeTimeout = setTimeout(() => {
		localStorage.setItem("volume", `${volume}`);
	}, SAVE_VOLUME_TIMEOUT_MS);
};
volumeSlider.value = 100;

meowAudio.onplay = () => {
	heartImg.style.display = "block";
	heartImg.style.animation = "1s linear 0s heart-animation";
	setTimeout(() => {
		heartImg.style.display = "none";
		heartImg.style.animation = "";
	}, 900);

	meowCount += 1;
	localStorage.setItem("meowCount", `${meowCount}`);

	if (meowCount === 100) {
		showNotification("a little chatty", "make milo meow 100 times", 5000);
		achievementUnlockedAudio.play();
		localStorage.setItem(
			"achievements",
			JSON.stringify([ACHIEVEMENT_A_LITTLE_CHATTY]),
		);
	}
};

// don't wanna jumpscare ppl meow
achievementUnlockedAudio.volume = 0.05;

window.addEventListener("offline", () => {
	ws = null;
});

window.addEventListener("online", () => {
	ws = connectToWebSocket();
});

loadMeowCount();
loadInitialVolume();
animateCat();
enableSpaceBarControl();
