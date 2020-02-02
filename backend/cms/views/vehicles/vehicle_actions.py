"""
A view representing an instance of a requestnt of interest. Requests can be added, changed or retrieved via this view.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from ...decorators import region_permission_required, staff_required
from ...models import Request, Vehicle

logger = logging.getLogger(__name__)


@login_required
@region_permission_required
@permission_required('cms.manage_requests', raise_exception=True)
def get_route(request, vehicle_id, region_slug, language_code):
    veh = Vehicle.objects.get(id=vehicle_id)
    reqs = Request.objects.get(assignedBus=vehicle_id)
    #print(veh.get_route())
    #print(reqs)

    messages.success(request, _('Route was successfully generated.'))

    return redirect('requests', **{
        'region_slug': region_slug,
        'language_code': language_code,
    })
