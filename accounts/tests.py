from rest_framework.test import APITestCase 
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()

# Create your tests here.
class TestUserRegistration(APITestCase):
    def setUp(self): #Arrange
        self.register_url = reverse('register') # get actual URL using url name
        self.user_data = {
            "username": "testuser",
            "email": "test000@example.com",
            "password": "strongpass123",
            "password2": "strongpass123",
        }
    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists()) #verify database
        self.assertEqual(response.data["message"], "User registered successfully!")

    def test_register_user_duplicate_username(self):
        # Create a user with the same username as above
        User.objects.create_user(username="testuser", email="test001@example.com", password="password123")

        # Try registering a new user with the same username
        data = {
            "username": "testuser",  # duplicate
            "email": "test2@example.com",
            "password": "anotherpassword123",
            "password2": "anotherpassword123"
        }
        response = self.client.post(self.register_url, data, format="json")
        #print(response.data) 
        # response.data: 'username': [ErrorDetail(string='A user with that username already exists.', code='unique')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

class TestUserLogin(APITestCase):   
    def setUp(self):
        ## create a user
        self.user = User.objects.create_user(username="testuser", email="test001@example.com", password="password123")
        self.login_url = reverse('login')

    def test_login_user_with_valid_credentials(self):
        valid_login_credentials= {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post(self.login_url, valid_login_credentials, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        
    def test_login_user_with_invalid_credentials(self):
        invalid_login_credentials= {
            "username": "testuser",
            "password": "wrongpass123",
        }
        response = self.client.post(self.login_url, invalid_login_credentials, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class TestUserProfile(APITestCase):
    def setUp(self):
        # Create and authenticate a test user
        ## create a user
        self.user = User.objects.create_user(username="testuser", email="test001@example.com", password="password123", bio="a test bio", skills="cooking, tutoring")

        # Create a token for the user
        self.token = Token.objects.create(user=self.user)
        # tell API test client to include the authorization header in every request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.profile_url = reverse('profile')

    def test_get_profile(self):
        response = self.client.get(self.profile_url, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check returned user profile data
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['bio'], self.user.bio)
        self.assertEqual(response.data['skills'], self.user.skills)

    def test_patch_profile(self):
        new_profile_data = {
            "bio": "updated test bio", 
            "skills": "updated skills"
        }
        response = self.client.patch(self.profile_url, new_profile_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check returned user profile data
        self.assertEqual(response.data['bio'], new_profile_data['bio'])
        self.assertEqual(response.data['skills'], new_profile_data['skills'])

    def test_put_profile(self):
        new_profile_data = {
            "bio": "updated test bio", 
            "skills": "updated skills",
            "interests": "updated interests",
            "city": "updated city",
            "state": "updated state",
            "zip_code": "updated zip_code"
        }
        response = self.client.put(self.profile_url, new_profile_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check returned user profile data
        self.assertEqual(response.data['bio'], new_profile_data['bio'])
        self.assertEqual(response.data['skills'], new_profile_data['skills'])
        self.assertEqual(response.data['interests'], new_profile_data['interests'])
        
    def test_put_profile_with_missing_fields(self):
        new_profile_data = {
            "bio": "updated test bio", 
            "skills": "updated skills",
            "interests": "updated interests",
            "city": "updated city",
        }
        response = self.client.put(self.profile_url, new_profile_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)