"""

Returns:
    [type]: [description]
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
from ...forms.pages import PageForm, PageTranslationForm
from ...models import Page, PageTranslation, Region, Language

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
@method_decorator(region_permission_required, name='dispatch')
class PageView(PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.view_pages'
    raise_exception = True

    template_name = 'pages/page_form.html'
    base_context = {
        'current_menu_item': 'pages',
        'PUBLIC': status.PUBLIC
    }

    def get(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get('region_slug'))

        language = Language.objects.get(code=kwargs.get('language_code'))

        # get page and translation objects if they exist
        page = Page.objects.filter(id=kwargs.get('page_id')).first()
        page_translation = PageTranslation.objects.filter(
            page=page,
            language=language,
        ).first()

        # Make form disabled if user has no permission to edit the page
        disabled = False
        if page:
            if page.archived:
                disabled = True
                messages.warning(request, _("You cannot edit this page because it is archived."))
            elif not request.user.has_perm('cms.edit_page', page):
                disabled = True
                messages.warning(request, _("You don't have the permission to edit this page, but you can propose changes and submit them for review instead."))
        else:
            if not request.user.has_perm('cms.edit_pages'):
                raise PermissionDenied

        page_form = PageForm(
            instance=page,
            region=region,
            language=language,
            disabled=disabled
        )
        page_translation_form = PageTranslationForm(
            instance=page_translation,
            disabled=disabled
        )

        return render(request, self.template_name, {
            **self.base_context,
            'page_form': page_form,
            'page_translation_form': page_translation_form,
            'page': page,
            'language': language,
            # Languages for tab view
            'languages': region.languages if page else [language],
        })

    # pylint: disable=too-many-branches,unused-argument
    def post(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get('region_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))

        page_instance = Page.objects.filter(id=kwargs.get('page_id')).first()
        page_translation_instance = PageTranslation.objects.filter(
            page=page_instance,
            language=language,
        ).first()

        if not request.user.has_perm('cms.edit_page', page_instance):
            raise PermissionDenied

        page_form = PageForm(
            request.POST,
            instance=page_instance,
            region=region,
            language=language,
        )
        page_translation_form = PageTranslationForm(
            request.POST,
            instance=page_translation_instance,
            region=region,
            language=language,
        )

        if page_translation_form.data.get('public') and 'public' in page_translation_form.changed_data:
            if not request.user.has_perm('cms.publish_page', page_instance):
                raise PermissionDenied

        # TODO: error handling
        if not page_form.is_valid() or not page_translation_form.is_valid():
            messages.error(request, _('Errors have occurred.'))
            return render(request, self.template_name, {
                **self.base_context,
                'page_form': page_form,
                'page_translation_form': page_translation_form,
                'page': page_instance,
                'language': language,
                # Languages for tab view
                'languages': region.languages if page_instance else [language],
            })

        if not page_form.has_changed() and not page_translation_form.has_changed():
            messages.info(request, _('No changes detected.'))
            return render(request, self.template_name, {
                **self.base_context,
                'page_form': page_form,
                'page_translation_form': page_translation_form,
                'page': page_instance,
                'language': language,
                # Languages for tab view
                'languages': region.languages if page_instance else [language],
            })

        page = page_form.save()
        page_translation = page_translation_form.save(
            page=page,
            user=request.user,
        )

        published = page_translation.status == status.PUBLIC
        if not page_instance:
            if published:
                messages.success(request, _('Page was successfully created and published.'))
            else:
                messages.success(request, _('Page was successfully created.'))
        elif not page_translation_instance:
            if published:
                messages.success(request, _('Translation was successfully created and published.'))
            else:
                messages.success(request, _('Translation was successfully created.'))
        else:
            if published:
                messages.success(request, _('Translation was successfully published.'))
            else:
                messages.success(request, _('Translation was successfully saved.'))

        return redirect('edit_page', **{
            'page_id': page.id,
            'region_slug': region.slug,
            'language_code': language.code,
        })
