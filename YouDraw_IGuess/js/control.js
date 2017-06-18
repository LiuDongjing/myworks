const MaxSeq = 1000000;
var currentSeq = 0;
var canvas, board;
var socket = new WebSocket("ws://liudongjing.cn:10961", "tcp");
function download(filename, img) {
    var pom = document.createElement('a');
    pom.setAttribute('href', img);
    pom.setAttribute('download', filename);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}
function getSeq() {
	var now = currentSeq;
	currentSeq = (currentSeq + 1) % MaxSeq;
	return now;
}
function triggerEvent(e) {
	if(e.command === undefined) {
		var e = $.Event(e.type, {pageX:e.pageX, pageY:e.pageY} );
		canvas.trigger(e);
	}
	else {
		if(e.command === "setcolor") {
			board.setColor(e.color);
		}
		else if(e.command === "setmode") {
			board.setMode(e.mode);
		}
		else if(e.command === "backward") {
			board.goBackInHistory();
		}
		else if(e.command === "forward") {
			board.goForthInHistory();
		}
		else if(e.command === "reset") {
			board.reset({ background: true });
		}
		else if(e.command === "setsize") {
			board.ctx.lineWidth = e.size;
		}
	}
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
	if(localMouse === true) {
	board = new DrawingBoard.Board('paint', {
		controls: [
			'Color',
			{ Size: { type: 'dropdown' } },
			{ DrawingMode: { filler: true } },
			'Navigation',
			'Download'
		],
		size: 2,
		background: "#fff",
		webStorage: false,
		enlargeYourContainer: true,
		localMouse: localMouse
	});}
	else {
		board = new DrawingBoard.Board('paint', {
			controls: [
				'Download'
			],
			size: 2,
			background: "#fff",
			webStorage: false,
			enlargeYourContainer: true,
			localMouse: localMouse
		});
	}
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
