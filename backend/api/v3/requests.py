from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cms.models import Request, Region
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
        region = get_object_or_404(Region, name=data["region"])
        request = Request(pinname =data.get["pinname"],wheelchair = data.get["wheelchair"],gender = data.get["gender"]
         ,medicalNeeds= data.get["medicalNeeds"],luggage = data.get["luggage"], isoMat= data.get["isoMat"], blanket= data.get["blanket"],jacket = data.get["jacket"]
         ,sleepingBag = data.get["sleepingBag"],children = data.get["children"],pets = data.get["pets"],group = data.get["group"],helpername = data.get["helpername"]
         ,phone = data.get["phone"],region = region,address = data.get["address"],postcode = data.get["postcode"],latitude = data.get["latitude"]
         ,longitude = data.get["longitude"])
        request.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)
