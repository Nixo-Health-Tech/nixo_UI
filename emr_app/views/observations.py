from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Observation


def observations_list(request):
    labs = Observation.objects.filter(patient__owner=request.user).order_by("-datetime")[:200]
    return render(request, "emr/observations_list.html", {"observations": labs})
