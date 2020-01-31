from django.http import JsonResponse

from cms.models import Vehicle, Region

def transform_vehicle(vehicle: Vehicle):
    return {
        'id': vehicle.id,
        'region': vehicle.region.slug,
        'type': vehicle.type,
        'licencePlate': vehicle.licencePlate,
        'seats': vehicle.seats,
        'backseats': vehicle.backSeats,
        'equipment': vehicle.equipment,
    }

def vehicles(request):
    _vehicles = Vehicle.objects.all()
    result = []
    for vehicle in _vehicles:
        result.append(transform_vehicle(vehicle))
    return JsonResponse(result, safe=False)  # Turn off Safe-Mode to allow serializing arrays
