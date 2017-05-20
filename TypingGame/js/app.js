
const app = new WHS.App([
	new WHS.ElementModule(
			{container: document.getElementById('app')}
	),
	new WHS.SceneModule(),
	new WHS.CameraModule({
		position: new THREE.Vector3(0, 0, 50)
	}),
	new WHS.RenderingModule({bgColor: 0x162129}),
	new WHS.ResizeModule()
]);

const sphere = new WHS.Sphere({ // Create sphere component.
	geometry: {
		radius: 3,
		widthSegments: 32,
		heightSegments: 32
	},
	material: new THREE.MeshBasicMaterial({
		color: new THREE.Color( 'red' )
	}),
	position: [0, 10, 0]
});

sphere.addTo(app); // Add sphere to world.

new WHS.Plane({
	geometry: {
		width: 100,
		height: 100
	},
	material: new THREE.MeshBasicMaterial({
		color: new THREE.Color( 'blue' )
	}),
	rotation: {
		x: -3.14 / 2
	}
}).addTo(app);
app.start();

$(document).ready(
	function () {
			document.getElementById("file-input")
			.addEventListener('change', readSingleFile, false);
	}
);

function readSingleFile(e) {
	var file = e.target.files[0];
	if (!file) {
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		var contents = e.target.result;
		displayContents(contents);
	};
	reader.readAsText(file);
}

function displayContents(contents) {
	var element = document.getElementById('file-content');
	element.innerHTML = contents;
}