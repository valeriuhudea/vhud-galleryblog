  // Activading Navbar fade and padding removal for scroll

$(window).scroll(function() {
	if ($(document).scrollTop() > 50) {
		$('.navbar').addClass('navbar-soft');
		console.log();
	} else {
		$('.navbar').removeClass('navbar-soft');
	}
});

$(document).on('click', '.nav-menu a, .mobile-nav a', function(e) {
if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
  var hash = this.hash;
  var target = $(hash);
  if (target.length) {
	e.preventDefault();

	if ($(this).parents('.nav-menu, .mobile-nav').length) {
	  $('.nav-menu .active, .mobile-nav .active').removeClass('activated');
	  $(this).closest('li').addClass('activated');
	}

	if (hash == '#header') {
	  $('#header').removeClass('header-top');
	  $("section").removeClass('section-show');
	  return;
	}

	if (!$('#header').hasClass('header-top')) {
	  $('#header').addClass('header-top');
	  setTimeout(function() {
		$("section").removeClass('section-show');
		$(hash).addClass('section-show');

	  }, 350);
	} else {
	  $("section").removeClass('section-show');
	  $(hash).addClass('section-show');
	}

	$('html, body').animate({
	  scrollTop: 0
	}, 350);

	if ($('body').hasClass('mobile-nav-active')) {
	  $('body').removeClass('mobile-nav-active');
	  $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
	  $('.mobile-nav-overly').fadeOut();
	}

	return false;

  }
}
});