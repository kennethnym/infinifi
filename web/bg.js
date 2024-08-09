const DOT_COLOR_LIGHT_MODE = "#dce0e8";
let DOT_COLOR_DARK_MODE = "#45475a";
const DOT_RADIUS = 1 * devicePixelRatio;

// theme variables
const rootStyles = document.documentElement.style;
console.log(rootStyles);

const changeThemeBtn = document.getElementById("theme-btn");
const themeModal = document.querySelector(".theme-modal");
const themes = {
	darkMode: [
		{
			name: "Gotham Theme",
			background: "#0C1014",
			textColor: "#98D1CE",
			highlight: "#1B2B34",
			baseColor: "#343D46",
		},
		{
			name: "Solarized Dark",
			background: "#002B36",
			textColor: "#839496",
			highlight: "#073642",
			baseColor: "#586e75",
		},
		{
			name: "Dracula",
			background: "#282A36",
			textColor: "#F8F8F2",
			highlight: "#44475A",
			baseColor: "#6272A4",
		},
		{
			name: "Material Dark",
			background: "#263238",
			textColor: "#FFFFFF",
			highlight: "#37474F",
			baseColor: "#80CBC4",
		},
		{
			name: "Monokai",
			background: "#272822",
			textColor: "#F8F8F2",
			highlight: "#49483E",
			baseColor: "#A6E22E",
		},
		{
			name: "Gruvbox Dark",
			background: "#282828",
			textColor: "#ebdbb2",
			highlight: "#3c3836",
			baseColor: "#b16286",
		},
	],
	lightThemes: [],
};

const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

let mouseX = 0;
let mouseY = 0;
let dotColor = "#dce0e8";

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
	ctx.fillStyle = dotColor;
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

if (window.matchMedia) {
	const query = window.matchMedia("(prefers-color-scheme: dark)");
	dotColor = query.matches ? DOT_COLOR_DARK_MODE : DOT_COLOR_LIGHT_MODE;

	query.addEventListener("change", (event) => {
		dotColor = event.matches ? DOT_COLOR_DARK_MODE : DOT_COLOR_LIGHT_MODE;
		drawPattern();
	});
}

resizeCanvas(window.innerWidth, window.innerHeight);
drawPattern();

changeThemeBtn.onmousedown = () => {
	themeModal.classList.add("active");
	displayThemes();
};

function displayThemes() {
	themeModal.innerHTML = "";
	// biome-ignore lint/complexity/noForEach: <biome wanted me to use for..of loop but foreach is better for readablity ig.>
	themes.darkMode.forEach((theme) => {
		const themeItem = document.createElement("div");
		themeItem.className = "theme-item";

		const themeName = document.createElement("div");
		themeName.className = "theme-name";
		themeName.innerText = theme.name;

		const themePreview = document.createElement("div");
		themePreview.className = "theme-preview";
		themePreview.style.background = theme.name;

		const themeColors = document.createElement("div");
		themeColors.className = "theme-colors";
		themeColors.style.background = theme.background;

		const colors = ["textColor", "highlight", "baseColor"];
		// biome-ignore lint/complexity/noForEach: <biome wanted me to use for..of loop but foreach is better for readablity ig.>
		colors.forEach((color) => {
			const colorDiv = document.createElement("div");
			colorDiv.style.background = theme[color];
			colorDiv.style.width = "20px";
			colorDiv.style.height = "20px";
			colorDiv.style.borderRadius = "50%";
			colorDiv.title = color;
			themeColors.appendChild(colorDiv);
		});

		themeItem.appendChild(themeName);
		themeItem.appendChild(themePreview);
		themeItem.appendChild(themeColors);
		themeModal.appendChild(themeItem);

		themeItem.onmouseover = () => {
			rootStyles.setProperty("--text", theme.textColor);
			rootStyles.setProperty("--surface0", theme.highlight);
			rootStyles.setProperty("--base", theme.background);
			DOT_COLOR_DARK_MODE = theme.highlight;
		};
		themeItem.onmousedown = () => {
			themeModal.classList.remove("active");
		};
	});
}
