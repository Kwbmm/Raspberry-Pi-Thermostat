$(document).ready(function(){
	$(document).foundation();
//	var page = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
//	switch(page){
//		case 'setProgram':
//		setProgram();
//		break;
//		case 'stats':
//		stats();
//		break;
//		default:
//		break;
//	}
});

$(window).load(function() {
	SetOffCanvasHeight();
}).resize(function() {
	SetOffCanvasHeight();
});

function SetOffCanvasHeight() {
	var height = $(window).height();
	var contentHeight = $(".off-canvas-content").height();
	if (contentHeight > height) { height = contentHeight; }

	$(".off-canvas-wrapper").height(height);
	$(".off-canvas-wrapper-inner").height(height);
	$(".off-canvas").height(height);
}