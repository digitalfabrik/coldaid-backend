"""
Expansion of API-Endpoints for the CMS
"""
from django.conf.urls import include, url

from .v3.languages import languages
from .v3.regions import regions
from .v3.accommodations import accommodations
from .v3.pages import pages
from .v3.single_page import single_page
from .v3.vehicles import vehicles


urlpatterns = [
    url(r'regions/$', regions, name='regions'),
    url(r'(?P<region_slug>[-\w]+)/', include([
        url(r'languages/$', languages),
        url(r'(?P<language_code>[-\w]+)/accommodations/$', accommodations),
        url(r'(?P<language_code>[-\w]+)/pages/$', pages),
        url(r'(?P<language_code>[-\w]+)/page/$', single_page),
    ])),
    url(r'vehicles/$', vehicles, name='vehicles'),
]
