from django.shortcuts import render

from money.models import Movement


def movements_list(request):
	movements = Movement.objects.all()
	return render(request, "money/movements_list.html", {
		"movements": movements,
	})
