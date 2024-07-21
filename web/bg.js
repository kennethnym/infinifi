const COLOR_SURFACE1 = "#dce0e8";
const DOT_RADIUS = 1 * devicePixelRatio;

const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

let mouseX = 0;
let mouseY = 0;

function resizeCanvas(width, height) {
	const devicePixelRatio = window.devicePixelRatio || 1;
	canvas.style.width = `${width}px`;
	canvas.style.height = `${height}px`;
	canvas.width = width * devicePixelRatio;
	canvas.height = height * devicePixelRatio;
}

function clearCanvas() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawDot(x, y) {
	const distance = Math.sqrt((x - mouseX) ** 2 + (y - mouseY) ** 2);
	const effectRadius = 100;
	const radius =
		DOT_RADIUS +
		2 *
			devicePixelRatio *
			((effectRadius - Math.min(distance, effectRadius)) / effectRadius);
	ctx.beginPath();
	ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
	ctx.fillStyle = COLOR_SURFACE1;
	ctx.fill();
}

function drawPattern() {
	clearCanvas();
	for (let x = 0; x < canvas.width; x += 10 * devicePixelRatio) {
		for (let y = 0; y < canvas.height; y += 10 * devicePixelRatio) {
			drawDot(x, y);
		}
	}
}

window.addEventListener("resize", () => {
	resizeCanvas(window.innerWidth, window.innerHeight);
	drawPattern();
});

window.addEventListener("mousemove", (event) => {
	mouseX = event.clientX * devicePixelRatio;
	mouseY = event.clientY * devicePixelRatio;
	drawPattern();
});

resizeCanvas(window.innerWidth, window.innerHeight);
drawPattern();
