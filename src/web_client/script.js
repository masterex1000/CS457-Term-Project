// const ws_url = "ws://localhost:8080";
const ws_url = "ws://" + location.host;

const all_views = ["nameprompt", "connect", "quiz", "error"];

var state = {
	username: "placeholder",
	recvBuffer: "",
	isWaitingForConnect: true
};

window.onload = function () {
	// document.getElementById("nameprompt").style.display = "flex";
	// // document.getElementById("nameprompt").style.display = "none";
	// document.getElementById("connect").style.display = "none";
	// // document.getElementById("connect").style.display = "flex";
	// document.getElementById("quiz").style.display = "none";
	// document.getElementById("error").style.display = "none";

	switchToView("nameprompt");
	// switchToView("quiz");
};

function submit_username() {
	state.username = document.getElementById("username").value;

	if (state.username == "") return;

	if (!isValidUsername(state.username)) {
		let error_e = document.getElementById("usrnm_error");

		error_e.style.display = "block";
		error_e.innerHTML = "Error: Invalid Username";
		return;
	}

	console.log(state.username);

	// document.getElementById("nameprompt").style.display = "none";
	// document.getElementById("connect").style.display = "flex";
	switchToView("connect");

	state.isWaitingForConnect = true;
	connect(ws_url);
}

function answerKeyDown(event) {
	if (event.code === "Enter")
		submitAnswer();
}



function submitAnswer() {
	let answer = document.getElementById("answer").value;

	let errorE = document.getElementById("answer-error");

	errorE.style.display = "none";

	try {
		atf = matchTrueOrFalse(answer);
		sendJSON(state.socket, { "type": "answer", "data": { "answer": atf } });
	} catch (e) {
		errorE.style.display = "flex";
	}

	// console.log("Sending answer " + answer);
	// sendJSON(state.socket, {"type": "answer", "data": {"answer": answer}});
}

function send_answer(socket, answer) {
	// Send message of form
	// {"type": "answer", "data": {"answer": "asdf"}}
}

function send_username(socket, username) {
	// Send Message of form
	// {"type": "answer", "data": "blahblah"}
}

function isValidUsername(str) {
	// Regular expression to match only alphanumeric and special characters, no spaces
	const regex = /^[\w!@#$%^&*()\-+=~`{}[\]|:;"'<>,.?/\\]+$/;
	return regex.test(str);
}

function connect(url) {
	socket = new WebSocket(url);

	state.socket = socket;

	socket.addEventListener('open', () => {
		sendJSON(socket, { "type": "username", "data": state.username });
	});

	socket.addEventListener('message', async (event) => {
		const text = await blobToUTF8(event.data);
		console.log("Message From Server:", text);

		state.recvBuffer += text;

		handleRecvMesssage();
	});

	socket.addEventListener('error', (error) => {
		console.error("WebSocket Error:", error);
		handleError(error);
	});

	socket.addEventListener('close', (event) => {
		console.log('WebSocket Connection Closed: ', event.reason);

		if (event.reason === "")
			handleError("Socket Disconnected");
		handleError(event.reason);
	});
}

function switchToView(view) {
	for (const v of all_views) {
		display = "none";
		if (v === view)
			display = "flex";

		document.getElementById(v).style.display = display;
	}
}

function handleError(msg) {
	switchToView("error");
	document.getElementById("err_page_err").innerText = msg;
}

function handleRecvMesssage() {
	let newlineIndex;
	while ((newlineIndex = state.recvBuffer.indexOf("\n")) !== -1) {
		const message = state.recvBuffer.slice(0, newlineIndex);
		state.recvBuffer = state.recvBuffer.slice(newlineIndex + 1);

		processMessage(message);
	}
}

function processMessage(message) {
	msg = JSON.parse(message);

	console.log(msg);

	if (state.isWaitingForConnect) {
		switchToView("quiz");
		state.isWaitingForConnect = false;
	}

	if (msg.type === "scores") {
		state.scores = msg.data;
		updateScores();
	}

	if (msg.type === "question") {
		state.question = msg.data;
		updateQuestion();
	}

	if (msg.type === "winner") {
		handleWinner(msg.data);
	}
}

function updateScores() {
	let scoreList = document.getElementById("score-list");

	// Remove existing children
	while (scoreList.lastElementChild) {
		scoreList.removeChild(scoreList.lastElementChild);
	}

	let arr = [];

	for (var key in state.scores) {
		if (state.scores.hasOwnProperty(key)) {
			arr.push( [ key, state.scores[key] ] );
		}
	}

	arr.sort((a, b) => b[1] - a[1]);

	// console.log(arr)

	let newTable = document.createElement("TABLE");

	for(let i = 0; i < arr.length; i++) {
		let row = newTable.insertRow(-1);
		
		let idx = row.insertCell(-1);
		let name = row.insertCell(-1);
		let score = row.insertCell(-1);

		idx.innerText = (i + 1) + ".";
		name.innerText = arr[i][0];
		score.innerText = arr[i][1];
	}

	scoreList.appendChild(newTable);
}

function updateQuestion() {
	document.getElementById("question-text").innerText = state.question.question;
	document.getElementById("answer").value = "";
	document.getElementById("quiz-score").innerText = state.question.currentScore;
}

function handleWinner(data) {
	state.question.currentScore = 0;
	updateQuestion(); // hacky way to update score

	document.getElementById("winner-name").innerText = data.username;
	document.getElementById("winner-points").innerText = data.score;

	document.getElementById("pop-over").style.opacity = 1;

	setTimeout(() => {
		document.getElementById("pop-over").style.opacity = 0;
	}, 5000);
}

function sendJSON(socket, json) {
	sendMessage(socket, JSON.stringify(json));
}

function sendMessage(socket, msg) {
	b = new Blob([msg, "\n"], { type: 'text/plain' });
	socket.send(b); // works as expected
}

async function blobToUTF8(blob) {
	const text = await blob.text();
	return text;
}

function matchTrueOrFalse(input) {
	// Normalize input: trim whitespace and convert to lowercase
	const normalizedInput = input.trim().toLowerCase();

	if (normalizedInput.length === 0) {
		throw new Error("Invalid input: must match 'true' or 'false'.");
	}

	// Match substrings for "true" and "false"
	if ("true".startsWith(normalizedInput)) {
		return true;
	} else if ("false".startsWith(normalizedInput)) {
		return false;
	} else {
		throw new Error("Invalid input: must match 'true' or 'false'.");
	}
}