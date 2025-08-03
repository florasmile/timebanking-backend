from django.urls import path

from bookings.models import Booking
from .views import BookingListCreateView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),

]
