from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cms.models import Request, Region, Vehicle
import json
def transform_request(request: Request):
    if request.assignedBus is None:
        return {
            'id': request.id,
            'pinname': request.pinname,
            'wheelchair': request.wheelchair,
            'gender': request.gender,
            'medicalNeeds': request.medicalNeeds,
            'luggage': request.luggage,
            'isoMat' : request.isoMat,
            'blanket' : request.blanket,
            'jacket' : request.jacket ,
            'sleepingBag' : request.sleepingBag ,
            'children': request.children,
            'pets': request.pets,
            'group': request.group,
            'helpername': request.helpername,
            'phone': request.phone,
            'region': request.region.slug,
            'address': request.address,
            'postcode': request.postcode,
            'city': request.city,
            'country': request.country,
            'latitude': request.latitude,
            'longitude': request.longitude,
            'archived': request.archived,
            'assignedBusId': "None"
        }
    return {
        'id': request.id,
        'pinname': request.pinname,
        'wheelchair': request.wheelchair,
        'gender': request.gender,
        'medicalNeeds': request.medicalNeeds,
        'luggage': request.luggage,
        'isoMat' : request.isoMat,
        'blanket' : request.blanket,
        'jacket' : request.jacket ,
        'sleepingBag' : request.sleepingBag ,
        'children': request.children,
        'pets': request.pets,
        'group': request.group,
        'helpername': request.helpername,
        'phone': request.phone,
        'region': request.region.slug,
        'address': request.address,
        'postcode': request.postcode,
        'city': request.city,
        'country': request.country,
        'latitude': request.latitude,
        'longitude': request.longitude,
        'archived': request.archived,
        'assignedBusId': request.assignedBus.id
    }

def requests(request):
    _requests = Request.objects.all()
    result = []
    for request in _requests:
        result.append(transform_request(request))
    return JsonResponse(result, safe=False)  # Turn off Safe-Mode to allow serializing arrays

@csrf_exempt
def newrequest(request):
    if request.method != 'POST':
        return HttpResponse(f'Invalid request method.', status=405)

    data = json.loads(request.body)
    data = data.get("data")
    data = json.loads(data)
    try:
        region = get_object_or_404(Region, name="Nürnberg")
        request = Request(pinname =data["pinname"],wheelchair = data["wheelchair"],gender = data["gender"]
         ,medicalNeeds= data["medicalNeeds"],luggage = data["luggage"], isoMat= data["isoMat"], blanket= data["blanket"],jacket = data["jacket"]
         ,sleepingBag = data["sleepingBag"],children = data["children"],pets = data["pets"],group = data["group"],helpername = data["helpername"]
         ,phone = data["phone"],region = region,address = data["address"],postcode = data["postcode"],latitude = data["latitude"]
         ,longitude = data["longitude"])
        request.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)

@csrf_exempt
def acceptrequest(request):
    if request.method != 'POST':
        return HttpResponse(f'Invalid request method.', status=405)

    data = json.loads(request.body)
    data = data.get("data")
    data = json.loads(data)
    try:
        requestobj = get_object_or_404(Request, id=data["id"])
        vehicle = get_object_or_404(Vehicle, id=data["vehicle"])
        requestobj.assignedBus = vehicle
        requestobj.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)

@csrf_exempt
def finishrequest(request):
    if request.method != 'POST':
        return HttpResponse(f'Invalid request method.', status=405)

    data = json.loads(request.body)
    data = data.get("data")
    data = json.loads(data)
    try:
        requestobj = get_object_or_404(Request, id=data["id"])
        requestobj.archived = True
        requestobj.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)
