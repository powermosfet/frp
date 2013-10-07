function inject_amount(n) {
	input = document.getElementById('id_amount');
	input.value = n;
}
function inject_category(c) {
	input = document.getElementById('id_category');
	input.value = c;
}
function inject_date(n) {
	input = document.getElementById('id_date');
	input.value = '' + month.getFullYear() + '-' + month.getMonth() + '-' + n
} 
function inject_date_from_calendar(e) {
	tag = e.target;
	n = tag.textContent.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	inject_date(n);
}

function inject_date_init() {
	$('.day').click(inject_date_from_calendar);
}

window.addEventListener('load', inject_date_init);
