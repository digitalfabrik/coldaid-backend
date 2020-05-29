from django.http import JsonResponse
from cms.models import Vehicle

def transform_vehicle(vehicle: Vehicle):
    return {
        'id': vehicle.id,
        'region': vehicle.region.slug,
        'type': vehicle.vehicle_type,
        'license_plate': vehicle.license_plate,
        'seats': vehicle.seats,
        'backseats': vehicle.backseats,
        'equipment': vehicle.equipment,
    }

def vehicles(request):
    _vehicles = Vehicle.objects.all()
    result = []
    for vehicle in _vehicles:
        result.append(transform_vehicle(vehicle))
    return JsonResponse(result, safe=False)  # Turn off Safe-Mode to allow serializing arrays
