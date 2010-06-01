$(document).ready(function() {
	var queryhash = window.location.hash
	switch (queryhash) {
		case "#about":
			document.title = "Scrabit - About";
			initialShowAbout();
			break;
		case "#contact":
			document.title = "Scrabit - Get Scrabit";
			initialShowGetScrabit();
			break;
		case "#networks":
			document.title = "Scrabit - Public Images";
			initialShowPublicImages();
			break;
		default:
			initialShowPublicImages();
			break;
	}
	$("h2").hide();
	$("#vcard a").hover(showVcardLabel, hideVcardLabel);
	$("#nav-about a").click(showAbout);
	$("#nav-networks a").click(showPublicImages);
	$("#nav-contact a").click(showGetScrabit);
});

function showVcardLabel() {
	$("#vcard a span").show();
	$("#vcard a span").animate({
		top: "-40px",
		opacity: 1
	}, 250 );
}

function hideVcardLabel() {
	$("#vcard a span").animate({ 
		top: "-35px",
		opacity: 0
	}, 250 );
	setTimeout("$('#vcard a span').hide();", 250);
	$("#vcard a span").animate({ 
		top: "-45px",
	}, 250 );
}

function initialShowPublicImages() {
	$("#content").hide();
	$("#timvandamme").removeClass();
	$("#timvandamme").addClass("networks");
	$(".node").hide();
	$("#networks").show();
	setTimeout("$('#content').slideDown('slow');", 1000);
}

function initialShowAbout() {
	$("#content").hide();
	$("#timvandamme").removeClass();
	$("#timvandamme").addClass("about");
	$(".node").hide();
	$("#about").show();
	setTimeout("$('#content').slideDown('slow');", 1000);
}

function initialShowGetScrabit() {
	$("#content").hide();
	$("#timvandamme").removeClass();
	$("#timvandamme").addClass("contact");
	$(".node").hide();
	$("#contact").show();
	setTimeout("$('#content').slideDown('slow');", 1000);
}

function showAbout() {
	if ($("#timvandamme").hasClass("about")){ }
	else {
		document.title = "Scrabit - About";
		$("#content").slideUp(500);
		$(".node").fadeOut(500);
		setTimeout("$('.node').hide();", 500);
		setTimeout("$('#about').show();", 500);
		$("#content").slideDown(500);
		$("#timvandamme").removeClass();
		$("#timvandamme").addClass("about");
	}
}

function showPublicImages() {
	document.title = "Scrabit - Public Images";
	if ($("#timvandamme").hasClass("networks")){ }
	else {
		$("#content").slideUp(500);
		$(".node").fadeOut(500);
		setTimeout("$('.node').hide();", 500);
		setTimeout("$('#networks').show();", 500);
		$("#content").slideDown(500);
		$("#timvandamme").removeClass();
		$("#timvandamme").addClass("networks");
	}
}

function showGetScrabit() {
	if ($("#timvandamme").hasClass("contact")){ }
	else {
		document.title = "Scrabit - Get Scrabit";
		$("#content").slideUp(500);
		$(".node").fadeOut(500);
		setTimeout("$('.node').hide();", 500);
		setTimeout("$('#contact').show();", 500);
		$("#content").slideDown(500);
		$("#timvandamme").removeClass();
		$("#timvandamme").addClass("contact");
	}
}
