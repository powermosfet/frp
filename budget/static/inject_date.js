function inject_date(e) {
	tag = e.target;
	n = tag.textContent.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	input = document.getElementById('id_date');
	input.value = '' + month.getFullYear() + '-' + month.getMonth() + '-' + n
}

function inject_date_init() {
	$('.day').click(inject_date);
}

window.addEventListener('load', inject_date_init);
