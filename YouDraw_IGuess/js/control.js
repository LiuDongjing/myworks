const MAX_SEQ = 1000000;
let currentSeq = 0;
let canvas, board;
let localMouse = true;
function download(filename, img) {
    let pom = document.createElement('a');
    pom.setAttribute('href', img);
    pom.setAttribute('download', filename);
    if (document.createEvent) {
        let event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}
function getSeq() {
	let now = currentSeq;
	currentSeq = (currentSeq + 1) % MAX_SEQ;
	return now;
}
function triggerEvent(e) {
	if(e.command === undefined) {
		let t = $.Event(e.type, {pageX:e.pageX, pageY:e.pageY} );
		canvas.trigger(t);
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
		    let e = JSON.parse(event.data);
        delayEvent(e);
		}
	}
}
function sendEvent(e) {
	socket.send(JSON.stringify(e));
}
function validate() {
  socket.onopen = (event) => {
    socket.send(JSON.stringify({'password':password}));
  }
  socket.onmessage = (event) => {
    let e = JSON.parse(event.data);
    console.log(e);
    if(e.command === 'sucess') {
      localMouse = e.role === 'producer';
      init();
    }
    else if (e.command === 'error'){
      alert(e.data);
    }
    else {
      console.log('数据传输错误！');
    }
  }
}
