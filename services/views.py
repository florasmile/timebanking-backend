from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Service
from .serializers import ServiceSerializer

# GET/POST 
# /services/
class ServiceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # List all services or filter by owner/zip code
    def get(self, request):
        owner_id = request.query_params.get('owner_id')
        zip_code = request.query_params.get('zip_code')
        queryset = Service.objects.all()
        if owner_id:
            queryset = queryset.filter(owner__id=owner_id)
        if zip_code:
            queryset = queryset.filter(owner__zip_code=zip_code)
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    # Create a new service
    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET/PATCH/DELETE 
# /services/<service_id>/
class ServiceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Retrieve a service by ID
    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    # Update a service (owner only)
    def patch(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        if service.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a service (owner only)
    def delete(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        if service.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        service.delete()
        return Response({'detail': 'Service deleted.'}, status=status.HTTP_204_NO_CONTENT)
