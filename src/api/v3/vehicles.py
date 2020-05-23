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

def vehicles(request, region_slug):
    _vehicles = Vehicle.objects.all()
    result = []
    for vehicle in _vehicles:
        if vehicle.region.slug == region_slug:
            result.append(transform_vehicle(vehicle))
    return JsonResponse(result, safe=False)  # Turn off Safe-Mode to allow serializing arrays
