function sort() {
	column = $(this).attr("class").split(' ')[0];
	$("#direction").remove();
	if ($(this).hasClass("desc")) {
		$("#html-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
		$(this).addClass("asc");
		reverse = -1;
	} else {
		$("#html-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
		$(this).addClass("desc");
		reverse = 1;
	}
	if (column == "name") {
		$(this).append('<img src="/.virtual/'+((reverse == 1) ? 'desc' : 'asc')+'.png" id="direction" />');
	} else {
		$(this).prepend('<img src="/.virtual/'+((reverse == 1) ? 'desc' : 'asc')+'.png" id="direction" />');
	}
	rows = $("#html-index-list tbody tr").detach()
	rows.sort(function(a, b) {
		result = $(a).data('type') - $(b).data('type')
		if (result != 0) { return result }

		return (($(a).data(column) < $(b).data(column)) - ($(a).data(column) > $(b).data(column))) * reverse

	});
	$("#html-index-list tbody").append(rows);
}

function prepare() {
	$("#html-index-list tbody tr").each(function(i) {
		if ($(this).children(".name").hasClass("back")) {
			$(this).data('type', 1);
		} else if ($(this).children(".name").hasClass("dir")) {
			$(this).data('type', 2);
		} else {
			$(this).data('type', 3);
		}
		$(this).data('name', $(this).children(".name").text().toLowerCase());
		$(this).data('size', parseInt($(this).children(".size").attr("sort")));
		$(this).data('date', parseInt($(this).children(".date").attr("sort")));
	});

	$("#html-index-list thead tr th").each(function(i) {
		$(this).bind('click', sort);
	});
}

$(document).ready(function(){
	prepare();
});