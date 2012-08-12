from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from money.forms import UploadCSVstatementForm
from money.models import Movement, MovementCategory


def movements_list(request):
	movements = Movement.objects.all()
	return render(request, "money/movements_list.html", {
		"movements": movements,
	})


def upload_estatement(request):
	form = UploadCSVstatementForm()

	if request.method == "POST":
		form = UploadCSVstatementForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('movements_list'))

	return render(request, "money/upload_estatement.html", {
		"form": form,
	})


@csrf_exempt  # TOOD very very wrong, temporary fix
def inline_category_edit(request):
	if request.is_ajax:
		category_id = request.POST["category"]
		movement_id = request.POST["movement"]

		movement = Movement.objects.get(pk=movement_id)
		if category_id == 'None':
			movement.category = None
		else:
			movement.category = MovementCategory.objects.get(pk=category_id)
		movement.save()
		return HttpResponse("Ok", content_type="text/plain")
	return HttpResponseForbidden()
