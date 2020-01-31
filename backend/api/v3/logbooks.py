from django.http import JsonResponse, HttpResponse
import json
from cms.models import Logbook, Region

def transform_logbook(logbook: Logbook):
    return {
        'id': logbook.id,
        'vehicle': logbook.vehicle.licencePlate,
        'driver': logbook.driver,
        'coDriver': logbook.coDriver,
        'startDate': logbook.startDate,
        'startMileage': logbook.startMileage,
        'endDate': logbook.endDate,
        'endMileage': logbook.endMileage,
        'comments': logbook.comments,
        'finished': logbook.finished
    }

def logbooks(request):
    _logbooks = Logbook.objects.all()
    result = []
    for logbook in _logbooks:
        result.append(transform_logbook(logbook))
    return JsonResponse(result, safe=False)  # Turn off Safe-Mode to allow serializing arrays
