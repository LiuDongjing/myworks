function init() {
	var customBoard2 = new DrawingBoard.Board('paint', {
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
		localMouse: true
	});
}