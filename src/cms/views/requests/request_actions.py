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
from ...models import Request

logger = logging.getLogger(__name__)


@login_required
@region_permission_required
@permission_required('cms.manage_requests', raise_exception=True)
def archive_request(request, request_id, region_slug):
    request1 = Request.objects.get(id=request_id)

    request1.archived = True
    request1.save()

    messages.success(request, _('Request was successfully archived.'))

    return redirect('requests', **{
                'region_slug': region_slug,
    })


@login_required
@region_permission_required
@permission_required('cms.manage_requests', raise_exception=True)
def restore_request(request, request_id, region_slug):
    request1 = Request.objects.get(id=request_id)

    request1.archived = False
    request1.save()

    messages.success(request, _('Request was successfully restored.'))

    return redirect('requests', **{
                'region_slug': region_slug,
    })


@login_required
@staff_required
def delete_request(request, request_id, region_slug):

    request1 = Request.objects.get(id=request_id)
    request1.delete()
    messages.success(request, _('Request was successfully deleted.'))

    return redirect('requests', **{
        'region_slug': region_slug,
    })


@login_required
@region_permission_required
@permission_required('cms.manage_requests', raise_exception=True)
# pylint: disable=unused-argument
def view_request(request, request_id, region_slug):
    template_name = 'requests/request_view.html'
    _request = Request.objects.get(id=request_id)

    #TODO does Request.objects.get() return None if there's no such request?
    #if not _request:
    #    raise Http404

    return render(
        request,
        template_name,
        {
            "request": _request
        }
    )
    