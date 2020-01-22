"""
File routing to the admin region
"""


from django.contrib import admin

from .models import Event
from .models import EventTranslation
from .models import Extra
from .models import ExtraTemplate
from .models import Language
from .models import LanguageTreeNode
from .models import Organization
from .models import Page
from .models import PageTranslation
from .models import POI
from .models import POITranslation
from .models import Region
from .models import RecurrenceRule
from .models import Logbook
from .models import Vehicle
admin.site.register(Event)
admin.site.register(EventTranslation)
admin.site.register(Extra)
admin.site.register(ExtraTemplate)
admin.site.register(Language)
admin.site.register(LanguageTreeNode)
admin.site.register(Logbook)
admin.site.register(Organization)
admin.site.register(Page)
admin.site.register(PageTranslation)
admin.site.register(POI)
admin.site.register(POITranslation)
admin.site.register(Region)
admin.site.register(RecurrenceRule)
admin.site.register(Vehicle)
