/*Плавный скроллинг к якорю*/
$(function() {
	$('a[data-target^="anchor"]').bind('click.smoothscroll' , function() {
		let target = $(this).attr('href'),
		bl_top = $(target).offset().top;
		$('body, html').animate({scrollTop: bl_top - 30} , 900);
		return false;
	})
});


$(function() {

	let $window = $(window);
	let inputSubmit = $('.subscribe input[type="submit"]');
	let inputMail = $('.subscribe input[type="email"]');

	if ($window.width() < 992 ) {
		inputSubmit.attr("value", "Subscribe");
		inputMail.attr("placeholder", "Type your e-mail");
	} else {
		inputSubmit.attr("value", "Subscribe now");
		inputMail.attr("placeholder", "Enter e-mail address");
	}

	$(window).resize(function(){

		if ($window.width() < 992 ) {
			inputSubmit.attr("value", "Subscribe");
			inputMail.attr("placeholder", "Type your e-mail");
		} else {
			inputSubmit.attr("value", "Subscribe now");
			inputMail.attr("placeholder", "Enter e-mail address");
		}
	});
});


$(function() {

	let $window = $(window);
	
	if ($window.width() < 575 ) {
		$( ".illustrations .inner" ).click(function(event) {
        event.stopPropagation();
});
	} 

	$(window).resize(function() {
if ($window.width() < 575 ) {
		$( ".illustrations .inner" ).click(function(event) {
        event.stopPropagation();
});
	} 
	})

});