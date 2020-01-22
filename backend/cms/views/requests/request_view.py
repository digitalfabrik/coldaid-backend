"""
A view representing an instance of a requestnt of interest. Requests can be added, changed or retrieved via this view.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...constants import status
from ...decorators import region_permission_required
from ...forms.requests import RequestForm, RequestTranslationForm
from ...models import Request, RequestTranslation, Region, Language

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
@method_decorator(region_permission_required, name='dispatch')
class RequestView(PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.manage_requests'
    raise_exception = True

    template_name = 'requests/request_form.html'
    base_context = {'current_menu_item': 'requests'}

    def get(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get('region_slug'))

        language = Language.objects.get(code=kwargs.get('language_code'))

        # get request and translation objects if they exist
        request = Request.objects.filter(id=kwargs.get('request_id')).first()
        request_translation = RequestTranslation.objects.filter(
            request=request,
            language=language,
        ).first()

        # Make form disabled if user has no permission to edit the page
        if not request.user.has_perm('cms.edit_requests'):
            disabled = True
            messages.warning(request, _("You don't have the permission to edit this Request."))
        elif request and request.archived:
            disabled = True
            messages.warning(request, _("You cannot edit this Request because it is archived."))
        else:
            disabled = False

        request_form = RequestForm(
            instance=request,
            disabled=disabled,
        )
        request_translation_form = RequestTranslationForm(
            instance=request_translation,
            disabled=disabled,
        )

        return render(request, self.template_name, {
            **self.base_context,
            'request_form': request_form,
            'request_translation_form': request_translation_form,
            'language': language,
            # Languages for tab view
            'languages': region.languages if request else [language],
        })

    # pylint: disable=too-many-branches,too-many-locals,unused-argument
    def post(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get('region_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))

        request_instance = Request.objects.filter(id=kwargs.get('request_id')).first()
        request_translation_instance = RequestTranslation.objects.filter(
            request=request_instance,
            language=language,
        ).first()

        request_form = RequestForm(
            request.POST,
            instance=request_instance,
        )
        request_translation_form = RequestTranslationForm(
            request.POST,
            instance=request_translation_instance,
            region=region,
            language=language,
        )

        if (
                not request_form.is_valid() or
                not request_translation_form.is_valid()
        ):

            # Add error messages
            for form in [request_form, request_translation_form]:
                for field in form:
                    for error in field.errors:
                        messages.error(request, _(field.label) + ': ' + _(error))
                for error in form.non_field_errors():
                    messages.error(request, _(error))

        elif (
                not request_form.has_changed() and
                not request_translation_form.has_changed()
        ):

            messages.info(request, _('No changes detected.'))

        else:

            if request_translation_form.instance.status == status.PUBLIC:
                if not request.user.has_perm('cms.publish_requests'):
                    raise PermissionDenied

            request = request_form.save(
                region=region,
            )
            request_translation = request_translation_form.save(
                request=request,
                user=request.user,
            )
            published = request_translation.public and 'public' in request_translation_form.changed_data
            if request_form.data.get('submit_archive'):
                # archive button has been submitted
                messages.success(request, _('Request was successfully archived.'))
            elif not request_instance:
                if published:
                    messages.success(request, _('Request was successfully created and published.'))
                else:
                    messages.success(request, _('Request was successfully created.'))
                    return redirect('edit_request', **{
                        'request_id': request.id,
                        'region_slug': region.slug,
                        'language_code': language.code,
                    })
            elif not request_translation_instance:
                if published:
                    messages.success(request, _('Request Translation was successfully created and published.'))
                else:
                    messages.success(request, _('Request Translation was successfully created.'))
            else:
                if published:
                    messages.success(request, _('Request Translation was successfully published.'))
                else:
                    messages.success(request, _('Request Translation was successfully saved.'))

        return render(request, self.template_name, {
            **self.base_context,
            'request_form': request_form,
            'request_translation_form': request_translation_form,
            'language': language,
            # Languages for tab view
            'languages': region.languages if request_instance else [language],
        })
