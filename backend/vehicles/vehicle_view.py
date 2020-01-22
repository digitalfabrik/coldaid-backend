"""
A view representing an instance of a vehiclent of interest. vehicles can be added, changed or retrieved via this view.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.http import HttpResponse
from ...constants import status
from ...decorators import region_permission_required, staff_required
from ...forms.vehicles import VehicleCreateForm
from ...models import Vehicle, Region, Language

logger = logging.getLogger(__name__)

def vehicle_list_view(request):
    queryset= Vehicle.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request,'vehicles/vehicle_list.html',context)

# pylint: disable=unused-argument
def vehicle_detail_view(request, vehicle_id):
    template_name = 'vehicles/vehicle_detail.html'
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)


    return render(
        request,
        template_name,
        {
            "vehicle": vehicle
        }
    )
def vehicle_create_view(request):
    form = VehicleCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = VehicleCreateForm()
        return redirect('/vehicles')
    context = {
        "form": form
    }
    return render(request,'vehicles/vehicle_create.html',context)

def vehicle_edit_view(request,vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    form = VehicleCreateForm(request.POST or None, instance=vehicle)
    if form.is_valid():
        vehicle.finished = True
        form.save()
        form = VehicleFinishForm()
        return redirect('../')
    context = {
        "form": form
    }
    return render(request,'vehicles/vehicle_create.html',context)
