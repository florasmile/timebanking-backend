from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    latitude = serializers.FloatField(source='owner.latitude', read_only=True)
    longitude = serializers.FloatField(source='owner.longitude', read_only=True)
    city=serializers.CharField(source='owner.city', read_only=True)
    zip_code=serializers.CharField(source='owner.zip_code', read_only=True)

    customer_reviews = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'category', 'service_type', 'description', 'tags', 'credit_required',
            'created_at', 'is_available', 'average_rating', 'total_sessions',
            'remaining_sessions', 'owner', 'owner_email', 'latitude', 'longitude', 'city', 'zip_code', 'customer_reviews'
        ]
        read_only_fields = [
            'id', 'created_at', 'owner', 'owner_email', 'average_rating',
            'remaining_sessions', 'is_available', 'latitude', 'longitude', 'city', 'zip_code', 'customer_reviews'
        ]

    def validate_average_rating(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Average rating must be between 0 and 5.")
        return value


    def create(self, validated_data):
        total_sessions = validated_data.get('total_sessions')
        # Set remaining_sessions to total_sessions
        validated_data['remaining_sessions'] = total_sessions
        return super().create(validated_data)