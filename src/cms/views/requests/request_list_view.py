from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from cms.models import Region

from ...decorators import region_permission_required


@method_decorator(login_required, name='dispatch')
@method_decorator(region_permission_required, name='dispatch')
class RequestListView(PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.manage_requests'
    raise_exception = True

    template = 'requests/request_list.html'
    template_archived = 'requests/request_list_archived.html'
    archived = False

    @property
    def template_name(self):
        return self.template_archived if self.archived else self.template

    def get(self, request, *args, **kwargs):
        # current region
        region_slug = kwargs.get('region_slug')
        region = Region.objects.get(slug=region_slug)

        return render(
            request,
            self.template_name,
            {
                'current_menu_item': 'requests',
                'requests': region.requests.filter(archived=self.archived),
                'archived_count': region.requests.filter(archived=True).count(),
            }
        )
