from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'category', 'description', 'tags', 'credit_required',
            'created_at', 'is_available', 'average_rating', 'total_sessions',
            'remaining_sessions', 'owner', 'owner_email'
        ]
        read_only_fields = ['id', 'created_at', 'owner', 'owner_email', 'average_rating', 'remaining_sessions', 'is_available']
