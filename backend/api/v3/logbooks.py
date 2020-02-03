from django.http import JsonResponse, HttpResponse
import json
from cms.models import Logbook, Region , Vehicle
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404


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

@csrf_exempt
def newlogbook(request):
    if request.method != 'POST':
        return HttpResponse(f'Invalid request method.', status=405)

    data = json.loads(request.body)
    data = data.get("data")
    data = json.loads(data)
    try:
        vehicle = get_object_or_404(Vehicle, id=data["vehicle"])
        logbook = Logbook(vehicle = vehicle,driver=data["driver"],coDriver=data["coDriver"],startMileage=int(data["startMileage"]),press= data["press"])
        logbook.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)

@csrf_exempt
def finishlogbook(request):
    if request.method != 'POST':
        return HttpResponse(f'Invalid request method.', status=405)

    data = json.loads(request.body)
    data = data.get("data")
    data = json.loads(data)
    try:
        logbook = get_object_or_404(Logbook, id=data["id"])
        logbook.endMileage = data["endMileage"]
        logbook.comments = data["comments"]
        logbook.finished = True
        logbook.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)
