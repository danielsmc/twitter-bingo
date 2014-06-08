$(document) .ready (function()
	{
	
	
	console.log('works');
	

	$('.bingo_grid li') .click (function ()
	{	
	$('#holder') .fadeOut (100);
	var width = $('.bingo_grid') .width ();	
	if (width < 550)
		{
		var contents = $(this) .clone ();
		$('#holder') .fadeIn (300);
		$('#holder li') .remove ();
		$('#holder') .append (contents);
		}
	});
	
	
	$('.close_box') .click (function ()
		{	
		$('#holder') .fadeOut (100);
		});
	
	
	
	
	});