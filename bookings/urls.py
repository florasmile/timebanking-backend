from django.urls import path
from .views import BookingListCreateView, BookingDetailView, MarkConfirmedView, MarkCompletedView, MarkCancelledView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:booking_id>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:booking_id>/mark_confirmed/', MarkConfirmedView.as_view(), name='booking-confirmed'),
    path('<int:booking_id>/mark_completed/', MarkCompletedView.as_view(), name='booking-completed'),
    path('<int:booking_id>/mark_cancelled/', MarkCancelledView.as_view(), name='booking-cancelled'),
]
