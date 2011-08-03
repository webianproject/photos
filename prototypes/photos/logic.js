$(document).ready(function(event) {
	$(".thumbnail_link").click(function() {
		$(this).children(":first").addClass('clicked');
	});
});
