var canvas, stage, exportRoot;

function init() {
	canvas = document.getElementById("canvas");
	images = images||{};

	var manifest = [
		{src:"img/canvas/bt.jpg", id:"bt"},
		{src:"img/canvas/hover_1.jpg", id:"hover_1"},
		{src:"img/canvas/hover_2.jpg", id:"hover_2"},
		{src:"img/canvas/khoi_000.png", id:"khoi_000"},
		{src:"img/canvas/khoi_001.png", id:"khoi_001"},
		{src:"img/canvas/khoi_002.png", id:"khoi_002"},
		{src:"img/canvas/khoi_003.png", id:"khoi_003"},
		{src:"img/canvas/khoi_004.png", id:"khoi_004"},
		{src:"img/canvas/khoi_005.png", id:"khoi_005"},
		{src:"img/canvas/khoi_006.png", id:"khoi_006"},
		{src:"img/canvas/khoi_007.png", id:"khoi_007"},
		{src:"img/canvas/khoi_008.png", id:"khoi_008"},
		{src:"img/canvas/khoi_009.png", id:"khoi_009"},
		{src:"img/canvas/khoi_010.png", id:"khoi_010"},
		{src:"img/canvas/khoi_011.png", id:"khoi_011"},
		{src:"img/canvas/khoi_012.png", id:"khoi_012"},
		{src:"img/canvas/khoi_013.png", id:"khoi_013"},
		{src:"img/canvas/khoi_014.png", id:"khoi_014"},
		{src:"img/canvas/mask.png", id:"mask"}
	];

	var loader = new createjs.LoadQueue(false);
	loader.addEventListener("fileload", handleFileLoad);
	loader.addEventListener("complete", handleComplete);
	loader.loadManifest(manifest);
}

function handleFileLoad(evt) {
	if (evt.item.type == "image") { images[evt.item.id] = evt.result; }
}

function handleComplete() {
	exportRoot = new lib.hover();

	stage = new createjs.Stage(canvas);
	stage.addChild(exportRoot);
	stage.update();

	createjs.Ticker.setFPS(24);
	createjs.Ticker.addEventListener("tick", stage);
}