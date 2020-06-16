"""
A view representing an instance of a request of interest. Requests can be added, changed or retrieved via this view.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...decorators import region_permission_required
from ...forms.requests import RequestForm
from ...models import Request, Region

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
@method_decorator(region_permission_required, name='dispatch')
class RequestView(PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.manage_requests'
    raise_exception = True

    template_name = 'requests/request_form.html'
    base_context = {'current_menu_item': 'requests'}

    def get(self, request, *args, **kwargs):

        # get request object if it exists
        _request = Request.objects.filter(id=kwargs.get('request_id')).first()

        if _request and _request.archived:
            messages.warning(request, _("You cannot edit this request because it is archived."))

        request_form = RequestForm(instance=_request)

        return render(request, self.template_name, {
            **self.base_context,
            'request_form': request_form,
        })

    # pylint: disable=too-many-branches,too-many-locals,unused-argument
    def post(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get('region_slug'))

        request_instance = Request.objects.filter(id=kwargs.get('request_id')).first()

        if request_instance and request_instance.archived:
            return redirect('edit_request', **{
                'request_id': request_instance.id,
                'region_slug': region.slug,
            })

        request_form = RequestForm(
            request.POST,
            instance=request_instance,
        )

        if not request_form.is_valid():
            # Add error messages
            for form in request_form:
                for field in form:
                    for error in field.errors:
                        messages.error(request, _(field.label) + ': ' + _(error))
                for error in form.non_field_errors():
                    messages.error(request, _(error))
        elif not request_form.has_changed():
            messages.info(request, _('No changes detected.'))
        else:
            _request = request_form.save(region=region)

            if not request_instance:
                messages.success(request, _('Request was successfully created.'))
                return redirect('edit_request', **{
                    'request_id': _request.id,
                    'region_slug': region.slug,
                })
            messages.success(request, _('Request was successfully saved.'))

        return render(request, self.template_name, {
            **self.base_context,
            'request_form': request_form,
        })
