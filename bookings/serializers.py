from rest_framework import serializers
from django.utils import timezone
from bookings.models import Booking
from services.models import Service

class BookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_first_name = serializers.CharField(source='owner.first_name', read_only=True)

    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'status',
            'booked_at',
            'completed_at',
            'customer_review',
            'customer_rating',
            'service_name',
            'owner_first_name',
            'owner_email',
            'customer_first_name',
            'customer_email'
        ]

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
        if service.remaining_sessions == 0:
            service.is_available = False
        service.save(update_fields=["remaining_sessions", "is_available"])

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

class BookingRatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer_rating', 'customer_review']

    def validate_customer_rating(self, value):
        if value is None:
            raise serializers.ValidationError("Rating is required.")
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value