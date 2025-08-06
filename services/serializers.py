from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    latitude = serializers.FloatField(source='owner.latitude', read_only=True)
    longitude = serializers.FloatField(source='owner.longitude', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'category', 'description', 'tags', 'credit_required',
            'created_at', 'is_available', 'average_rating', 'total_sessions',
            'remaining_sessions', 'owner', 'owner_email', 'latitude', 'longitude'
        ]
        read_only_fields = ['id', 'created_at', 'owner', 'owner_email', 'average_rating', 'remaining_sessions', 'is_available', 'latitude', 'longitude']
        
    def create(self, validated_data):
        total_sessions = validated_data.get('total_sessions')
        # Set remaining_sessions to total_sessions
        validated_data['remaining_sessions'] = total_sessions
        return super().create(validated_data)