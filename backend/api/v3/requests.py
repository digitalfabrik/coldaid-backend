from django.http import JsonResponse

from cms.models import Request, Region

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
