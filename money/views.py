from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from money.forms import UploadCSVstatementForm
from money.models import Movement


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
