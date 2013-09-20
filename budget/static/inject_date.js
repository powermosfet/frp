function inject_date(n) {
	input = document.getElementById('date_field');
	input.value = zero_pad(n) + '.' + zero_pad(month) + '.' + year;
}

function zero_pad(n) {
	if(n < 10) {
		return '0' + n;
	} else {
		return '' + n;
	}
}

function inject_date_create_func(n) {
	return function() { inject_date( n ); };
}

function inject_date_init() {
	for(i = 1; i <= 31; i++) {
		linkId = 'day' + i;
		e = document.getElementById(linkId);
		e.addEventListener('click', inject_date_create_func(i) );
	}
}

window.addEventListener('load', inject_date_init);
