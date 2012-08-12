$(".categoryInline").change(function(event){
	var movement = $("#id_movement", this).attr("value");
	var category = $(this).find("option:selected").attr("value");
	$.ajax({
		type: "POST",
		url: "/banking/movement/edit/category/",
		data: {
			movement: movement,
			category: category
		}
	})
});