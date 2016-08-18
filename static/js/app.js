$(document).ready(function(){
	$(document).foundation();
	var page = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
	switch(page){
		case 'monday':
		setProgram();
		break;
		case 'tuesday':
		setProgram();
		break;
		case 'wednesday':
		setProgram();
		break;
		case 'thursday':
		setProgram();
		break;
		case 'friday':
		setProgram();
		break;
		case 'saturday':
		setProgram();
		break;
		case 'sunday':
		setProgram();
		break;
//		case 'stats':
//		stats();
//		break;
		default:
		break;
	}
});

//$(window).load(function() {
//	SetOffCanvasHeight();
//}).resize(function() {
//	SetOffCanvasHeight();
//});

function SetOffCanvasHeight() {
	var height = $(window).height();
	var contentHeight = $(".off-canvas-content").height();
	if (contentHeight > height) { height = contentHeight; }

	$(".off-canvas-wrapper").height(height);
	$(".off-canvas-wrapper-inner").height(height);
	$(".off-canvas").height(height);
}

function setProgram() {
	/*
	Add the animation and control for the + and - buttons
	*/
	$('i.fi-minus').click(function(){
		var thisID = $(this).attr('id'); //Get the ID of this element
		var thisArrayID = thisID.split("-"); //Split the ID
		var hour = thisArrayID[1];
		var $currentTempShownItem = $('span#showDeg-'+hour); //<span> showing the temp
		var currentTempShown = parseInt($currentTempShownItem.text()); //Get the value
		var $currentTempHiddenItem = $('input#dataDeg-'+hour); //<input> storing the value
		currentTempShown = currentTempShown > 0 ? currentTempShown-1 : 0;
		$currentTempHiddenItem.attr('value',currentTempShown); //Save the new value in the hidden <input>
		$currentTempShownItem
			.html("<i class='fi-arrow-down'></i>"+currentTempShown+"°C")
			.removeClass('secondary alert')
			.addClass('info')
			.switchClass('info','secondary',2000);
		$currentTempShownItem.children('i').fadeOut(2000, function(){$(this).css('visibility', 'hidden').css('display','');});
	});
	$('i.fi-plus').click(function(){
		var thisID = $(this).attr('id');
		var thisArrayID = thisID.split("-");
		var hour = thisArrayID[1];
		var $currentTempShownItem = $('span#showDeg-'+hour);
		var $currentTempHiddenItem = $('input#dataDeg-'+hour);
		var currentTempShown = parseInt($currentTempShownItem.text());
		currentTempShown = currentTempShown < 30 ? currentTempShown+1 : 30;
		$currentTempHiddenItem.attr('value',currentTempShown);
		$currentTempShownItem
			.html("<i class='fi-arrow-up'></i>"+currentTempShown+"°C")
			.removeClass('secondary info')
			.addClass('alert')
			.switchClass('alert','secondary',2000);
		$currentTempShownItem.children('i').fadeOut(2000, function(){$(this).css('visibility', 'hidden').css('display','');});
	});

	/*
	Set some padding-top for the hour and the temperature elements so that they are vertically
	centered.
	*/
	//Get the height of the div that contains the +/- controls
	var controlsHeight = $('span.alert.badge.medium').parent().height();
	$('span.hour,span[id^="showDeg-"]').each(function(){
		var selfHeight = $(this).css('height');
		var diff = parseInt(controlsHeight) - parseInt(selfHeight);
		var padding = diff/2;
		$(this).parent().css({'padding-top':padding});
	});
}