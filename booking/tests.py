from datetime import datetime, timedelta
from booking.models import Booking


def find_free_times(room_id, start_date, end_date):
    bookings = Booking.objects.filter(room_id=room_id, planed_from__gte=start_date, planed_to__lte=end_date).order_by(
        'planed_from')

    free_times = []
    current_time = start_date

    for booking in bookings:
        if booking.planed_from > current_time:
            free_times.append({
                'start': current_time,
                'end': booking.planed_from
            })
        current_time = max(current_time, booking.planed_to)

    if current_time < end_date:
        free_times.append({
            'start': current_time,
            'end': end_date
        })

    return free_times
