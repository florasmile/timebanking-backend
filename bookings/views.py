from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
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
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookingSerializer
        return BookingCreateSerializer
    # list all bookings belongs to an owner/customer and status
    def get(self, request):
        owner_id = request.query_params.get('owner_id')
        customer_id = request.query_params.get('customer_id')
        status = request.query_params.get('status')

        queryset = Booking.objects.all()

        if owner_id:
            queryset = queryset.filter(owner__id=owner_id)
        if customer_id:
            queryset = queryset.filter(customer__id=customer_id)
        if status:
            queryset = queryset.filter(status=status)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

# GET/PATCH
# /bookings/<booking_id>