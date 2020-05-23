"""
File routing to the admin region
"""


from django.contrib import admin

from .models import Accommodation
from .models import AccommodationTranslation
from .models import Beds
from .models import BedTargetGroup
from .models import Event
from .models import EventTranslation
from .models import Offer
from .models import OfferTemplate
from .models import Language
from .models import LanguageTreeNode
from .models import Organization
from .models import Page
from .models import PageTranslation
from .models import POI
from .models import POITranslation
from .models import Region
from .models import RecurrenceRule
from .models import Vehicle
from .models import Request
from .models import RequestTranslation

admin.site.register(Accommodation)
admin.site.register(AccommodationTranslation)
admin.site.register(Beds)
admin.site.register(BedTargetGroup)
admin.site.register(Event)
admin.site.register(EventTranslation)
admin.site.register(Offer)
admin.site.register(OfferTemplate)
admin.site.register(Language)
admin.site.register(LanguageTreeNode)
admin.site.register(Organization)
admin.site.register(Page)
admin.site.register(PageTranslation)
admin.site.register(POI)
admin.site.register(POITranslation)
admin.site.register(Region)
admin.site.register(RecurrenceRule)
admin.site.register(Vehicle)
admin.site.register(Request)
admin.site.register(RequestTranslation)
