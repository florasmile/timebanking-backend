from django.urls import path
from .views import ServiceListCreateView, ServiceDetailView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'),
    path('<int:service_id>/', ServiceDetailView.as_view(), name='service-detail'),
]
