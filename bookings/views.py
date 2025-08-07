from operator import countOf
from django.forms import IntegerField
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg  # For aggregation

# Create your views here.

from drf_spectacular.utils import extend_schema, extend_schema_view

# GET/POST
# /bookings/
@extend_schema(
    request=BookingCreateSerializer,
    responses={201: BookingSerializer, 400: dict},
    methods=["POST"],
    description="Create a booking if customer has enough time credits and service has remaining sessions."
)
@extend_schema(
    responses={200: BookingSerializer(many=True)},
    methods=["GET"],
    description="List bookings filtered by owner_id, customer_id, or status."
)
class BookingListCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # get serializer class dynamically
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookingSerializer
        return BookingCreateSerializer
    # list all bookings belongs to an owner/customer and status
    def get(self, request):
        # print("Query Params:", request.query_params)
        owner_id = request.query_params.get('owner_id')
        customer_id = request.query_params.get('customer_id')
        status = request.query_params.get('status')

        # print("Filtered Customer ID:", customer_id)
        # start with empty queryset
        queryset = Booking.objects.none()
        
        if owner_id:
            if str(request.user.id) != owner_id:
                return Response({"detail": "You are not allowed to view other users' bookings."}, status=403)
            queryset = Booking.objects.filter(owner__id=owner_id)
        elif customer_id:
            if str(request.user.id) != customer_id:
                return Response({"detail": "You are not allowed to view other users' bookings."}, status=403)
            queryset = Booking.objects.filter(customer__id=customer_id)
        else:
            return Response({"detail": "Please provide either owner_id or customer_id."}, status=400)
        
        # print("All bookings for customer:", Booking.objects.filter(customer__id=customer_id))
        # filter by status
        if status:
            queryset = queryset.filter(status=status)

        serializer = self.get_serializer(queryset, many=True)
        # print("serializer.data", serializer.data)
        return Response(serializer.data)
    
    #only customer is allowed to create a booking
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           

# GET/PATCH
# /bookings/<booking_id>
class BookingDetailView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = self.serializer_class(booking)
        return Response(serializer.data)

    # add customer_rating and reviews to booking
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        service = booking.service

        if booking.customer != request.user:
            raise PermissionDenied("Only the customer can rate and review this booking.")
        # Validate required fields
        if 'customer_rating' not in request.data:
            return Response(
                {"detail": "Customer_rating must be provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            customer_rating = int(request.data['customer_rating'])
            if not (1 <= customer_rating <= 5):  # Assuming 5-star rating system
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"detail": "Rating must be an integer between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.customer_rating = customer_rating
        # update average_rating for service
        completed_bookings = Booking.objects.filter(
            service=booking.service,
            status='completed',
            customer_rating__isnull=False
        )
        service.average_rating = completed_bookings.aggregate(
            avg_rating=Avg('customer_rating')
        )['avg_rating'] or 0.0
        
        service.save()

        # update customer_review
        if 'customer_review' in request.data:
            customer_review = request.data['customer_review']
            if not isinstance(customer_review, str) or not customer_review.strip():
                return Response(
                    {"detail": "Review must be a non-empty string"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            booking.customer_review = customer_review.strip()
            # add to the customer_reviews list of the service model later
            booking.save()

            return Response({"detail": "Booking updated successfully"}, status=200)

# change status
@extend_schema(
    methods=["PATCH"],
    responses={200: BookingSerializer}
)
class MarkConfirmedView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        # Ensure only the owner can confirm the booking
        if booking.owner != request.user:
            raise PermissionDenied("Only the service owner can confirm this booking.")

        if booking.status != "pending":
            return Response({"detail": "Booking must be in 'pending' state."}, status=400)
        booking.status = "confirmed"
        booking.save()
        return Response({"detail": "Booking confirmed."}, status=200)
    
class MarkCompletedView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        # Ensure only the customer can confirm the booking
        if booking.customer != request.user:
            raise PermissionDenied("Only the customer can confirm the completion of this booking.")
        if booking.status != "confirmed":
            return Response({"detail": "Booking must be in 'confirmed' state."}, status=400)
        # add time_credits to owner
        owner = booking.owner
        service = booking.service
        owner.time_credits += service.credit_required
        owner.save()

        booking.status = "completed"
        booking.completed_at = timezone.now()

        # save data
        booking.save()
        
        return Response({"detail": "Booking completed."}, status=200)

class MarkCancelledView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        
        # ensure only the booking owner or customer has the permission to cancel the booking
        if (request.user != booking.owner) and (request.user != booking.customer):
            raise PermissionDenied("Only the owner or customer can cancel this booking.")
        if (booking.status != "pending") and (booking.status !="confirmed"):
            return Response({"detail": "Booking must be in 'pending' or 'confirmed' state."}, status=400)
        # refund time_credits to customer
        customer = booking.customer
        service = booking.service
        customer.time_credits += service.credit_required
        customer.save()

        # add remaining_sessions back by 1 to service
        service.remaining_sessions += 1
        service.save()

        booking.status = "cancelled"
        booking.completed_at = timezone.now()

        # save data
        booking.save()
        
        return Response({"detail": "Booking cancelled and credits refunded."}, status=200)


