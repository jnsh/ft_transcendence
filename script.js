const canvas = document.getElementById("pong");
const ctx = canvas.getContext("2d");

const padleThic = 10;
const padleLen = 100;
const padleSpeed = 6;
var leftPadleY = (canvas.height - padleLen) / 2;
var rightPadleY = (canvas.height - padleLen) / 2;

var paddleMoveDown = false;
var paddleMoveUp = false;

const ballSize = 10;
var ballX = 0 + padleThic;
var ballY = canvas.height / 2;

var ballSpeed = 10;
var ballSpeedX = ballSpeed;
var ballSpeedY = 0;
var ballDirectionX = 1;
var ballDirectionY = 1;

var ballDirection = 0;

var scores = [0, 0];

var targetY = 0;

var pressedKeys = [];
window.addEventListener('keydown', keyPressEvent, false);
window.addEventListener('keyup', keyReleaseEvent, false);

function keyPressEvent(event) {
	pressedKeys[event.keyCode] = true;
	if (event.keyCode == 87)
		paddleMoveUp = true;
	else if (event.keyCode == 83)
		paddleMoveDown = true;
}

function keyReleaseEvent(event) {
	pressedKeys[event.keyCode] = false;
	if (event.keyCode == 87)
		paddleMoveUp = false;
	else if (event.keyCode == 83)
		paddleMoveDown = false;
}

function drawScore() {
	ctx.fillStyle = "#ddd";
	ctx.font = "40px Arial";
	var score = scores[0] + " : " + scores[1];
	ctx.fillText(score, canvas.width / 2 - ctx.measureText(score).width / 2, 50);
}

function drawBallSpeed() {
	ctx.fillStyle = "#ddd";
	ctx.font = "15px Arial";
	ctx.fillText("Ball Speed: " + Math.round(ballSpeed * 100) / 100, 2, 14);
}

function drawBall() {
	ctx.fillStyle = "#ddd";
	ctx.fillRect(ballX, ballY, ballSize, ballSize);
}

function drawLeftPadle() {
	ctx.fillStyle = "#ddd";
	ctx.fillRect(0, leftPadleY, padleThic, padleLen);
}

function drawRightPadle() {
	ctx.fillStyle = "#ddd";
	ctx.fillRect(canvas.width - padleThic, rightPadleY, padleThic, padleLen);
}

function updateBallPosition() {
	if (ballX <= 0) {
		scores[1]++;
		ballX = canvas.width;
		ballY = canvas.height / 2;
		ballDirection = 1;
		ballSpeed = 10;
	}
	else if (ballX >= canvas.width) {
		scores[0]++;
		ballX = 0 + ballSize;
		console.log("HIT: ", ballY, rightPadleY); //delete
		ballY = canvas.height / 2;
		ballDirection = 0;
		ballSpeed = 10;
	}

	if ((ballX <= padleThic && ballDirectionX == -1 && ballY + ballSize > leftPadleY && ballY < leftPadleY + padleLen) ||
		(ballX >= canvas.width - padleThic - ballSize && ballDirectionX == 1 && ballY + ballSize > rightPadleY && ballY < rightPadleY + padleLen)) {
		if (paddleMoveUp)
			ballDirectionY = -1;
		else if (paddleMoveDown)
			ballDirectionY = 1;
		else
			ballDirectionY = Math.random() < 0.5 ? -1 : 1;
		//ballDirectionY = Math.random() < 0.5 ? -1 : 1;
		ballDirectionX *= -1;
		ballSpeedY = Math.floor(Math.random() * ballSpeed);
		ballSpeedX = Math.sqrt((ballSpeed ** 2) - (ballSpeedY ** 2));

		ballDirection = ballDirection == 0 ? 1 : 0;
	}

	if (ballY <= 0 || ballY >= canvas.height - ballSize)
		ballDirectionY *= -1;

	ballX += ballSpeedX * ballDirectionX;
	ballY += ballSpeedY * ballDirectionY;
}

function updatePadlePosition() {
	// W
	if (pressedKeys[87] && leftPadleY > 0)
		leftPadleY -= padleSpeed;
	// S
	if (pressedKeys[83] && leftPadleY < canvas.height - padleLen)
		leftPadleY += padleSpeed;
	// Up Arrow
	if (pressedKeys[38] && rightPadleY > 0 && targetY < rightPadleY)
		rightPadleY -= padleSpeed;
	// Down Arrow
	if (pressedKeys[40] && rightPadleY < canvas.height - padleLen && targetY > rightPadleY + padleLen / 2)
		rightPadleY += padleSpeed;
}

// function getRandomNumber(min, max) {
// 	return Math.floor(Math.random() * (max - min + 1)) + min;
// }

function predictBallY() {
	var tempBallX = ballX;
	var tempBallY = ballY;
	var tempBallSpeedX = ballSpeedX;
	var tempBallSpeedY = ballSpeedY;
	var tempBallDirectionX = ballDirectionX;
	var tempBallDirectionY = ballDirectionY;

	while (tempBallX < canvas.width - padleThic) {
		tempBallX += tempBallSpeedX * tempBallDirectionX;
		tempBallY += tempBallSpeedY * tempBallDirectionY;

		if (tempBallY <= 0 || tempBallY >= canvas.height - ballSize) {
			tempBallDirectionY *= -1;
			tempBallY += tempBallSpeedY * tempBallDirectionY;
		}
	}
	return tempBallY;
}

function updateAIPadle() {
	if (ballDirection == 0) {
		targetY = predictBallY();
		console.log("PREDICT", targetY); //delete

		// make errros ...

		pressedKeys[38] = false;
		pressedKeys[40] = false;
		if (targetY < rightPadleY + padleLen / 2 - 25) {
			pressedKeys[38] = true;
			pressedKeys[40] = false;
		}
		else if (targetY > rightPadleY + padleLen / 2 + 25) {
			pressedKeys[38] = false;
			pressedKeys[40] = true;
		}
		else {
			pressedKeys[38] = false;
			pressedKeys[40] = false;
		}
		console.log("padle y: ", rightPadleY); //delete
	}
	if (ballDirection == 1) {
			//maybe shouuld move to the center!!!
			pressedKeys[38] = false;
			pressedKeys[40] = false;
	}
}

function draw() {
	updatePadlePosition();
	updateBallPosition();

	ctx.clearRect(0, 0, canvas.width, canvas.height);
	drawScore();
	drawBallSpeed();
	drawLeftPadle();
	drawRightPadle();
	drawBall();

	ballSpeed += 0.001;

	requestAnimationFrame(draw);
}

setInterval(updateAIPadle, 1000);

draw();
