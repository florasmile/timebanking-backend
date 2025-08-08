from django.db.models import Avg

def update_service_average(service):
    """
    Recompute and save Service.average_rating using only completed bookings
    with valid ratings (1-5). Clamps to [0, 5] and rounds to 1 decimal.
    """
    agg = service.bookings.filter(
        status='completed',
        customer_rating__isnull=False,
        customer_rating__gte=1,
        customer_rating__lte=5
    ).aggregate(avg=Avg('customer_rating'))

    avg = agg['avg'] or 0.0
    avg = max(0.0, min(5.0, round(avg, 1)))
    service.average_rating = avg
    service.save(update_fields=['average_rating'])
