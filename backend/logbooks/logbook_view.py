"""
A view representing an instance of a logbooknt of interest. Logbooks can be added, changed or retrieved via this view.
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
from ...forms.logbooks import LogbookCreateForm,LogbookFinishForm
from ...models import Logbook, Region, Language

logger = logging.getLogger(__name__)

def logbook_list_view(request):
    queryset= Logbook.objects.all().order_by('-startDate')
    context = {
        "object_list": queryset
    }
    return render(request,'logbooks/logbook_list.html',context)

# pylint: disable=unused-argument
def logbook_detail_view(request, logbook_id):
    template_name = 'logbooks/logbook_detail.html'
    logbook = get_object_or_404(Logbook, id=logbook_id)


    return render(
        request,
        template_name,
        {
            "logbook": logbook
        }
    )
def logbook_create_view(request):
    form = LogbookCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = LogbookCreateForm()
        return redirect('/logbooks')
    context = {
        "form": form
    }
    return render(request,'logbooks/logbook_create.html',context)

def logbook_finish_view(request,logbook_id):
    logbook = get_object_or_404(Logbook, id=logbook_id)
    form = LogbookFinishForm(request.POST or None, instance=logbook)
    if form.is_valid():
        logbook.finished = True
        form.save()
        form = LogbookFinishForm()
        return redirect('../')
    context = {
        "form": form
    }
    return render(request,'logbooks/logbook_finish.html',context)
