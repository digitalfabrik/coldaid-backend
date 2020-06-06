import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cms.models import Request, Region


def transform_request(request: Request):
    if request.assigned_bus is None:
        return {
            'id': request.id,
            'pinname': request.pinname,
            'wheelchair': request.wheelchair,
            'gender': request.gender,
            'medical_needs': request.medical_needs,
            'luggage': request.luggage,
            'iso_mat' : request.iso_mat,
            'blanket' : request.blanket,
            'jacket' : request.jacket ,
            'sleeping_bag' : request.sleeping_bag ,
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
            'assigned_bus_id': "None"
        }
    return {
        'id': request.id,
        'pinname': request.pinname,
        'wheelchair': request.wheelchair,
        'gender': request.gender,
        'medical_needs': request.medical_needs,
        'luggage': request.luggage,
        'iso_mat' : request.iso_mat,
        'blanket' : request.blanket,
        'jacket' : request.jacket,
        'sleeping_bag' : request.sleeping_bag,
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
        'assigned_bus_id': request.assigned_bus.id
    }

def requests(request):
    _requests = Request.objects.all()
    result = []
    for r in _requests:
        result.append(transform_request(r))
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
        request = Request(pinname=data["pinname"], wheelchair=data["wheelchair"], gender=data["gender"],
                          medical_needs=data["medical_needs"], luggage=data["luggage"], iso_mat=data["iso_mat"],
                          blanket=data["blanket"], jacket=data["jacket"], sleeping_bag=data["sleeping_bag"], children=data["children"],
                          pets=data["pets"], group=data["group"], helpername=data["helpername"], phone=data["phone"], region=region,
                          address=data["address"], postcode=data["postcode"], latitude=data["latitude"], longitude=data["longitude"]
                          )
        request.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type='text/plain', status=400)
