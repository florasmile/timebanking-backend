from rest_framework import serializers
from django.utils import timezone
from bookings.models import Booking
from services.models import Service
from services.serializers import ServiceSerializer
from accounts.serializers import UserProfileSerializer

class BookingSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    customer = UserProfileSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'status',
            'booked_at',
            'completed_at',
            'customer_review',
            'customer_rating',
            'owner',
            'customer',
            'service',
        ]
        read_only_fields = fields  

class BookingCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(write_only=True) 
    class Meta:
        model = Booking
        fields = ['service_id'] 
        read_only_fields = ['status', 'booked_at', 'owner', 'customer']

    def create(self, validated_data):
        request = self.context['request']
        customer = request.user
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)

        # check if customer has enough time_credits
        if customer.time_credits < service.credit_required:
            raise serializers.ValidationError("Not enough time credits to book this service.")

        # check if the service has remaining sessions (can remove if we only display available services)
        if service.remaining_sessions <= 0:
            raise serializers.ValidationError("No remaining sessions available for this service.")
        
                # Deduct time credits
        customer.time_credits -= service.credit_required
        customer.save()

        # Deduct one session from the service
        service.remaining_sessions -= 1
        service.save()

        #create a booking
        booking = Booking.objects.create(
            service=service,
            customer=customer,
            owner=service.owner,  
            booked_at=timezone.now(),
            status='pending',
            **validated_data
        )

        return booking