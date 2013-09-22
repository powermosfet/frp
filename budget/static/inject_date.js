function inject_date(e) {
	tag = e.target;
	n = tag.textContent.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	input = document.getElementById('date_field');
    date = new Date(year, month, n);
	input.value = date.toISOString().substr(0,10);
}

function zero_pad(n) {
	if(n < 10) {
		return '0' + n;
	} else {
		return '' + n;
	}
}

function inject_date_init() {
	$('.day').click(inject_date);
}

window.addEventListener('load', inject_date_init);
