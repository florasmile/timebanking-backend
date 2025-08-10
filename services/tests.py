from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Service

User = get_user_model()

class TestServiceEndpoints(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(email="user1@test.com", password="password123")
        self.user2 = User.objects.create_user(email="user2@test.com", password="password123")
        # Tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        # Auth header for user1 (owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        # Service creation data
        self.service_data = {
            "name": "Dog Sitting",
            "category": ["pets"],
            "description": "Take care of your dog for a day.",
            "service_type": "in-person",
            "tags": ["dog", "pet"],
            "credit_required": 1,
            "total_sessions": 3
        }
        # Create a service for user1
        self.service = Service.objects.create(
            owner=self.user1,
            name="Guitar Lessons",
            category=["music"],
            description="Learn guitar from scratch.",
            service_type="virtual",
            tags=["guitar", "music"],
            credit_required=2,
            total_sessions=5,
            remaining_sessions=5,
        )
        self.service_detail_url = reverse('service-detail', args=[self.service.id])
        self.service_list_url = reverse('service-list-create')

    def test_list_services(self):
        # test without owner_id param - result should not include user1's service, expect empty list
        response = self.client.get(self.service_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        # self.assertEqual(response.data[0]['name'], self.service.name)

        # create a service for user 2
        service2 = Service.objects.create(
            owner=self.user2,
            name="Piano Lessons",
            category=["music"],
            description="Learn piano from scratch.",
            service_type="virtual",
            tags=["piano", "music"],
            credit_required=3,
            total_sessions=10,
            remaining_sessions=10,
        )
        # test without owner_id param - should see service2 only
        response = self.client.get(self.service_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], service2.name)

        # test with owner_id pram - should see owner1's service only
        response = self.client.get(self.service_list_url, {'owner_id': self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.service.name)

        # Test with owner_id parameter for user2 - should show only user2's services
        response = self.client.get(self.service_list_url, {'owner_id': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], service2.name)

    def test_create_service(self):
        response = self.client.post(self.service_list_url, self.service_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Service.objects.filter(name="Dog Sitting", owner=self.user1).exists())
        self.assertEqual(response.data["remaining_sessions"], self.service_data["total_sessions"])

    def test_retrieve_service(self):
        response = self.client.get(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.service.name)
        self.assertEqual(response.data["owner"], self.user1.id)

    def test_update_service_owner_only(self):
        patch_data = {"description": "Updated description!"}
        # Owner can update
        response = self.client.patch(self.service_detail_url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], patch_data["description"])
        # Non-owner should be forbidden
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.patch(self.service_detail_url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_service_owner_only(self):
        # Owner can delete
        response = self.client.delete(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Service.objects.filter(id=self.service.id).exists())
        # Re-create service for further tests
        self.service = Service.objects.create(
            owner=self.user1,
            name="Temp Service",
            category=["temp"],
            description="Temporary.",
            service_type="virtual",
            tags=["temp"],
            credit_required=1,
            total_sessions=1,
            remaining_sessions=1,
        )
        url = reverse('service-detail', args=[self.service.id])
        # Non-owner cannot delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Remove auth
        # List
        response = self.client.get(self.service_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Create
        response = self.client.post(self.service_list_url, self.service_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Retrieve
        response = self.client.get(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service_invalid(self):
        bad_data = self.service_data.copy()
        bad_data["credit_required"] = 0  # Invalid, must be >=1
        response = self.client.post(self.service_list_url, bad_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("credit_required", response.data)

