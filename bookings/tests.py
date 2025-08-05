from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from services.models import Service
from bookings.models import Booking

User = get_user_model()

class TestBookingEndpoints(APITestCase):
    def setUp(self):
        # Create service owner and customer
        self.owner = User.objects.create_user(email="owner@test.com", password="password123", time_credits=0)
        self.customer = User.objects.create_user(email="customer@test.com", password="password123", time_credits=10)
        self.other_user = User.objects.create_user(email="other@test.com", password="password123", time_credits=10)

        # Tokens
        self.owner_token = Token.objects.create(user=self.owner)
        self.customer_token = Token.objects.create(user=self.customer)
        self.other_token = Token.objects.create(user=self.other_user)

        # Create service (needs to exist for booking)
        self.service = Service.objects.create(
            owner=self.owner,
            name="Dog Walking",
            category=["pets"],
            description="Walk your dog",
            service_type="in-person",
            tags=["dog", "walk"],
            credit_required=2,
            total_sessions=3,
            remaining_sessions=3,
        )

        # Booking URLs
        self.booking_list_url = reverse('booking-list-create')

    def test_create_booking_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        data = {"service_id": self.service.id}
        response = self.client.post(self.booking_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(customer=self.customer, service=self.service).exists())
        booking = Booking.objects.get(customer=self.customer, service=self.service)
        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.owner, self.owner)
        # Customer credits decreased
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.time_credits, 8)
        # Service remaining_sessions decreased
        self.service.refresh_from_db()
        self.assertEqual(self.service.remaining_sessions, 2)

    def test_create_booking_insufficient_credits(self):
        # Set customer credits too low
        self.customer.time_credits = 1
        self.customer.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        data = {"service_id": self.service.id}
        response = self.client.post(self.booking_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not enough time credits", str(response.data))

    def test_create_booking_no_sessions(self):
        self.service.remaining_sessions = 0
        self.service.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        data = {"service_id": self.service.id}
        response = self.client.post(self.booking_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No remaining sessions available", str(response.data))

    def test_list_bookings_by_customer(self):
        # Create a booking for this customer
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = f"{self.booking_list_url}?customer_id={self.customer.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], booking.id)

    def test_list_bookings_by_owner(self):
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        url = f"{self.booking_list_url}?owner_id={self.owner.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_bookings_permission_denied(self):
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        # Other user tries to list bookings for customer
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        url = f"{self.booking_list_url}?customer_id={self.customer.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_booking_detail(self):
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        url = reverse('booking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], booking.id)

    def test_mark_confirmed_owner_only(self):
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        url = reverse('booking-confirmed', args=[booking.id])
        # Owner can confirm
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "confirmed")
        # Customer cannot confirm
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_completed_customer_only(self):
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="confirmed"
        )
        url = reverse('booking-completed', args=[booking.id])
        # Customer can complete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "completed")
        # Owner cannot complete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_cancelled_owner_or_customer(self):
        # Owner can cancel
        booking1 = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        url1 = reverse('booking-cancelled', args=[booking1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.patch(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking1.refresh_from_db()
        self.assertEqual(booking1.status, "cancelled")
        # Customer can cancel
        booking2 = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        url2 = reverse('booking-cancelled', args=[booking2.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.patch(url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking2.refresh_from_db()
        self.assertEqual(booking2.status, "cancelled")
        # Other user cannot cancel
        booking3 = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        url3 = reverse('booking-cancelled', args=[booking3.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.patch(url3, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Remove credentials
        self.client.credentials()
        # Create booking
        response = self.client.post(self.booking_list_url, {"service_id": self.service.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # List bookings
        url = f"{self.booking_list_url}?customer_id={self.customer.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Booking detail
        booking = Booking.objects.create(
            service=self.service,
            customer=self.customer,
            owner=self.owner,
            status="pending"
        )
        url = reverse('booking-detail', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
