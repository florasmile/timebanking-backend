import os
import django
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from accounts.models import User

def create_seed_users():
    demo_users = [
        {
            "email": "alex.johnson@example.com",
            "first_name": "Alex",
            "last_name": "Johnson",
            "bio": "Software engineer and amateur chef",
            "skills": "Python, Cooking, Photography",
            "interests": ["hiking", "coding"],
            "time_credits": 5.0,
            "street": "123 Tech Lane",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.6062,
            "longitude": -122.3321
        },
        {
            "email": "maria.garcia@example.com",
            "first_name": "Maria",
            "last_name": "Garcia",
            "bio": "Graphic designer and yoga instructor",
            "skills": "Photoshop, Yoga Instruction, Spanish",
            "interests": ["painting", "meditation"],
            "time_credits": 8.0,
            "street": "456 Art Street",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
            "latitude": 30.2672,
            "longitude": -97.7431
        },
        {
            "email": "jamal.williams@example.com",
            "first_name": "Jamal",
            "last_name": "Williams",
            "bio": "High school math teacher",
            "skills": "Mathematics, Tutoring, Basketball",
            "interests": ["sports", "reading"],
            "time_credits": 3.0,
            "street": "789 Education Blvd",
            "city": "Chicago",
            "state": "IL",
            "zip_code": "60601",
            "latitude": 41.8781,
            "longitude": -87.6298
        },
        # Add 7 more users following the same pattern
        {
            "email": "sophia.chen@example.com",
            "first_name": "Sophia",
            "last_name": "Chen",
            "bio": "Professional musician and language tutor",
            "skills": "Piano, Mandarin, French",
            "interests": ["music", "languages"],
            "time_credits": 7.0,
            "street": "321 Harmony Ave",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        {
            "email": "david.kim@example.com",
            "first_name": "David",
            "last_name": "Kim",
            "bio": "Gardening expert and home renovator",
            "skills": "Landscaping, Carpentry, Plumbing",
            "interests": ["gardening", "DIY"],
            "time_credits": 10.0,
            "street": "654 Green Thumb Rd",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97201",
            "latitude": 45.5051,
            "longitude": -122.6750
        }
    ]

    for user_data in demo_users:
        user = User.objects.create_user(
            email=user_data["email"],
            password="demopass123",  # Standard password for all demo users
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            bio=user_data["bio"],
            skills=user_data["skills"],
            interests=user_data["interests"],
            time_credits=user_data["time_credits"],
            street=user_data["street"],
            city=user_data["city"],
            state=user_data["state"],
            zip_code=user_data["zip_code"],
            latitude=user_data["latitude"],
            longitude=user_data["longitude"]
        )
        print(f"Created user: {user.email}")

    print("Successfully created demo users!")

if __name__ == '__main__':
    create_seed_users()