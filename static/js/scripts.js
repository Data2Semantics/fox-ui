$(document).ready(function() { 
	populate_examples();
});

function populate_examples() {
	var examples = ['movies.psl', 'extended-movies.psl', 'feature-complete.psl'];
	$.each(examples, function(index, example) {
		var item = '<li role="presentation"><a role="menuitem" tabindex="-1" href="#" onclick="loadExample(\'' + example + '\')">' + example + '</a></li>';
		$('#examples-menu').append(item);
	});
}

function loadExample(filename) {
	// var url = 'http://localhost:5000/static/examples/' + filename;
	var url = '/static/examples/' + filename;
	console.log(url);
	$.get(url, function(data) {
		$('#code').val(data);
	});
}