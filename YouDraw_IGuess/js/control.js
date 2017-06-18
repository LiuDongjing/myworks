const MaxSeq = 1000000;
var currentSeq = 0;
var canvas;
var socket = new WebSocket("ws://liudongjing.cn:10961", "tcp");
function getSeq() {
	var now = currentSeq;
	currentSeq = (currentSeq + 1) % MaxSeq;
	return now;
}
function triggerEvent(e) {
	var e = $.Event(e.type, {pageX:e.pageX, pageY:e.pageY} );
	canvas.trigger(e);
	getSeq();
}
function delayEvent(e) {
	if(currentSeq < e.id) {
		setTimeout(delayEvent, e.id-currentSeq, e);
	}
	else {
		setTimeout(triggerEvent, 0, e);
	}
}
function init() {
	var board = new DrawingBoard.Board('paint', {
		controls: [
			'Color',
			{ Size: { type: 'dropdown' } },
			{ DrawingMode: { filler: true } },
			'Navigation',
			'Download'
		],
		size: 2,
		background: "#fff",
		webStorage: 'session',
		enlargeYourContainer: true,
		localMouse: localMouse
	});
	canvas = $("canvas");
	if(!board.localMouse) {
		socket.onmessage = function (event) {
		    var e = JSON.parse(event.data);
			delayEvent(e);
		}
	}
	var id;
	if(localMouse) {
		id = 'producer';
	}
	else {
		id = 'consumer';
	}
	socket.onopen = function (event) {
		socket.send(id);
	}
}
function sendEvent(e) {
	socket.send(JSON.stringify(e));
}
