var socket = new WebSocket("ws://liudongjing.cn:10961", "tcp");
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
	var canvas = $("canvas");
	if(!board.localMouse) {
		socket.onmessage = function (event) {
			console.log(event.data);
		    var e = JSON.parse(event.data);
			var e = $.Event(e.type, {pageX:e.pageX, pageY:e.pageY} );
			canvas.trigger(e);
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
//setInterval(function(){
