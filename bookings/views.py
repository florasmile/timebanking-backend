from operator import countOf
from django.forms import IntegerField
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingRatingReviewSerializer
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg  # For aggregation
from services.utils import update_service_average # Helper function

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
    
    
# change status
@extend_schema(
    methods=["PATCH"],
    responses={200: BookingSerializer}
)
class MarkConfirmedView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        # Ensure only the owner can confirm the booking
        if booking.owner != request.user:
            raise PermissionDenied("Only the service owner can confirm this booking.")

        if booking.status != "pending":
            return Response({"detail": "Booking must be in 'pending' state."}, status=400)
        booking.status = "confirmed"
        booking.save()
        serializer = self.serializer_class(booking)
        return Response(serializer.data)
    
@extend_schema(request=BookingRatingReviewSerializer, description="Set booking status to 'completed' and update rating/review.")
class MarkCompletedView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        # Ensure only the customer can confirm the booking
        if booking.customer != request.user:
            raise PermissionDenied("Only the customer can confirm the completion of this booking.")
        if booking.status != "confirmed":
            return Response({"detail": "Booking must be in 'confirmed' state."}, status=400)
        # validate request data
        serializer = BookingRatingReviewSerializer(
            booking,
            data=request.data,
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        # add time_credits to owner
        owner = booking.owner
        service = booking.service
        owner.time_credits += service.credit_required
        owner.save()

        #update booking status
        booking.status = "completed"
        booking.completed_at = timezone.now()

        # add customer_review
        if 'customer_review' in request.data:
            customer_review = request.data['customer_review']
            if customer_review.strip():                
                booking.customer_review = customer_review.strip()
                service.customer_reviews.append(customer_review)
                service.save(update_fields=['customer_reviews'])
        # add customer_rating
        booking.customer_rating = request.data['customer_rating']
        booking.save()
        update_service_average(service)
        
        serializer = self.serializer_class(booking)
        return Response(serializer.data)

class MarkCancelledView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
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
        
        serializer = self.serializer_class(booking)
        return Response(serializer.data)


