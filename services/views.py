from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Service
from .serializers import ServiceSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
# GET/POST 
# /services/
@extend_schema_view(
    get=extend_schema(responses=ServiceSerializer(many=True))
)
class ServiceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializer

    def get(self, request):
        # allows users to view a list of services created by themselves
        owner_id = request.query_params.get('owner_id')
        queryset = Service.objects.all()
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        # allow users to view services provided by others (but not themselves)
        else:
            queryset = queryset.exclude(owner_id=request.user.id)
            
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # Create a new service
    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET/PATCH/DELETE 
# /services/<service_id>/
class ServiceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializer
    # Retrieve a service by ID
    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        serializer = self.serializer_class(service)
        return Response(serializer.data)

    # Update a service (owner only)
    def patch(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        if service.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(service, data=request.data, partial=True)
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
