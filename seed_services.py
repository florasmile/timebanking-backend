import os
import django
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import random
from datetime import timedelta
from django.utils import timezone
from accounts.models import User
from services.models import Service

def create_seed_services():
    # Get all demo users (created from previous seed)
    demo_users = User.objects.filter(email__contains="@example.com")
    if not demo_users.exists():
        print("Please run user seeding first!")
        return

    service_templates = [
        {
            "name": "Yoga Instruction",
            "category": ["fitness", "wellness"],
            "description": "Beginner-friendly yoga sessions tailored to your needs",
            "service_type": "in-person",
            "tags": ["flexibility", "stress-relief"],
            "credit_required": 1.5
        },
        {
            "name": "Python Tutoring",
            "category": ["education", "technology"],
            "description": "Personalized Python programming lessons for all levels",
            "service_type": "virtual",
            "tags": ["coding", "web-development"],
            "credit_required": 2.0
        },
        {
            "name": "Home Gardening Help",
            "category": ["home", "outdoors"],
            "description": "Expert advice on plant care and garden design",
            "service_type": "in-person",
            "tags": ["plants", "landscaping"],
            "credit_required": 1.0
        },
        {
            "name": "Graphic Design",
            "category": ["creative", "business"],
            "description": "Logo design and branding assistance",
            "service_type": "virtual",
            "tags": ["logos", "branding"],
            "credit_required": 3.0
        },
        {
            "name": "Spanish Conversation Practice",
            "category": ["education", "language"],
            "description": "Improve your Spanish through casual conversation",
            "service_type": "virtual",
            "tags": ["language-learning", "español"],
            "credit_required": 1.0
        },
        # Add 15 more service templates...
        {
            "name": "Bicycle Repair",
            "category": ["repair", "outdoors"],
            "description": "Basic bicycle maintenance and repair services",
            "service_type": "in-person",
            "tags": ["bikes", "maintenance"],
            "credit_required": 2.0
        },
        {
            "name": "Meal Prep Guidance",
            "category": ["food", "health"],
            "description": "Weekly meal planning and healthy recipes",
            "service_type": "virtual",
            "tags": ["nutrition", "cooking"],
            "credit_required": 1.5
        },
        {
            "name": "Resume Review",
            "category": ["career", "business"],
            "description": "Professional feedback on your resume and cover letter",
            "service_type": "virtual",
            "tags": ["job-search", "career-advice"],
            "credit_required": 1.0
        },
        {
            "name": "Pet Sitting",
            "category": ["animals", "home"],
            "description": "Reliable care for your pets while you're away",
            "service_type": "in-person",
            "tags": ["dogs", "cats"],
            "credit_required": 1.0
        },
        {
            "name": "Music Lessons",
            "category": ["arts", "education"],
            "description": "Beginner guitar or piano lessons",
            "service_type": "in-person",
            "tags": ["guitar", "piano"],
            "credit_required": 2.0
        },
        {
            "name": "Python Programming Tutoring",
            "category": ["education", "technology", "tutoring"],
            "description": "One-on-one Python lessons for beginners to advanced coders",
            "service_type": "virtual",
            "tags": ["coding", "web-development"],
            "credit_required": 2.0
        },
        {
            "name": "Home Gardening Help",
            "category": ["home", "outdoors"],
            "description": "Expert advice on urban gardening and plant care",
            "service_type": "in-person",
            "tags": ["plants", "sustainability"],
            "credit_required": 1.5
        },
        {
            "name": "Yoga Instruction",
            "category": ["fitness", "wellness"],
            "description": "Personalized yoga sessions for all skill levels",
            "service_type": "in-person",
            "tags": ["flexibility", "stress-relief"],
            "credit_required": 1.5
        },
        {
            "name": "Graphic Design Consultation",
            "category": ["creative", "business"],
            "description": "Logo design and branding assistance",
            "service_type": "virtual",
            "tags": ["logos", "branding"],
            "credit_required": 2.0
        },
        {
            "name": "Bicycle Maintenance",
            "category": ["repair", "transportation"],
            "description": "Basic tune-ups and repair services",
            "service_type": "in-person",
            "tags": ["bikes", "sustainability"],
            "credit_required": 1.0
        },
        {
            "name": "Spanish Conversation Practice",
            "category": ["education", "language"],
            "description": "Improve your Spanish through casual conversation",
            "service_type": "virtual",
            "tags": ["language-learning", "español"],
            "credit_required": 1.0
        },
        {
            "name": "Meal Prep Guidance",
            "category": ["food", "health"],
            "description": "Weekly meal planning and healthy recipes",
            "service_type": "virtual",
            "tags": ["nutrition", "cooking"],
            "credit_required": 1.5
        },
        {
            "name": "Interior Design Consultation",
            "category": ["home", "creative"],
            "description": "Space planning and decor recommendations",
            "service_type": "in-person",
            "tags": ["home-decor", "organization"],
            "credit_required": 2.0
        },
        {
            "name": "Music Lessons (Guitar)",
            "category": ["arts", "education"],
            "description": "Beginner guitar lessons tailored to your interests",
            "service_type": "in-person",
            "tags": ["music", "guitar"],
            "credit_required": 2.0
        },
        {
            "name": "Social Media Strategy",
            "category": ["business", "marketing"],
            "description": "Content planning and growth strategies",
            "service_type": "virtual",
            "tags": ["instagram", "tiktok"],
            "credit_required": 2.5
        },
        {
            "name": "Senior Companion Visits",
            "category": ["community", "health"],
            "description": "Friendly visits and light assistance for seniors",
            "service_type": "in-person",
            "tags": ["eldercare", "companionship"],
            "credit_required": 1.0
        },
        {
            "name": "Photography Session",
            "category": ["arts", "professional"],
            "description": "Portrait or product photography services",
            "service_type": "in-person",
            "tags": ["portraits", "headshots"],
            "credit_required": 3.0
        },
        {
            "name": "Financial Planning Basics",
            "category": ["business", "education"],
            "description": "Budgeting and investment starter guidance",
            "service_type": "virtual",
            "tags": ["money-management", "investing"],
            "credit_required": 2.0
        },
        {
            "name": "Home Organization Help",
            "category": ["home", "lifestyle"],
            "description": "Closet and space organization strategies",
            "service_type": "in-person",
            "tags": ["decluttering", "konmari"],
            "credit_required": 1.5
        },
        {
            "name": "Public Speaking Coaching",
            "category": ["business", "education"],
            "description": "Overcome stage fright and improve presentations",
            "service_type": "virtual",
            "tags": ["communication", "confidence"],
            "credit_required": 2.0
        },
        {
            "name": "Car Maintenance Tutorial",
            "category": ["automotive", "education"],
            "description": "Basic car care and maintenance demonstrations",
            "service_type": "in-person",
            "tags": ["oil-change", "car-care"],
            "credit_required": 1.5
        },
        {
            "name": "Knitting/Crochet Lessons",
            "category": ["arts", "crafts"],
            "description": "Learn basic stitches and project planning",
            "service_type": "in-person",
            "tags": ["yarn-crafts", "handmade"],
            "credit_required": 1.0
        },
        {
            "name": "Hiking Guide",
            "category": ["outdoors", "fitness"],
            "description": "Guided hikes in local parks with safety tips",
            "service_type": "in-person",
            "tags": ["nature", "trails"],
            "credit_required": 1.0
        },
        {
            "name": "Video Editing Tutorial",
            "category": ["technology", "creative"],
            "description": "Basic video editing in Adobe Premiere",
            "service_type": "virtual",
            "tags": ["youtube", "content-creation"],
            "credit_required": 2.5
        },
        {
            "name": "Furniture Assembly Help",
            "category": ["home", "labor"],
            "description": "IKEA and other furniture assembly assistance",
            "service_type": "in-person",
            "tags": ["handyman", "home-improvement"],
            "credit_required": 1.0
        },
    ]

    # Create 45 services with random owners
    for i in range(45):
        template = random.choice(service_templates)
        owner = random.choice(demo_users)
        
        # Vary created_at dates over past 3 months
        created_at = timezone.now() - timedelta(days=random.randint(0, 90))
        
        total_sessions = random.randint(1, 20)
        service = Service.objects.create(
            owner=owner,
            name=template["name"],
            category=template["category"],
            description=template["description"],
            service_type=template["service_type"],
            tags=template["tags"],
            credit_required=template["credit_required"],
            created_at=created_at,
            is_available=True,
            total_sessions=total_sessions,
            remaining_sessions=random.randint(1, total_sessions),
            average_rating=round(random.uniform(3.5, 5.0), 1)
        )
        
        # Add some reviews if available
        if service.is_available:
            review_count = random.randint(0, 3)
            reviews = [
                "Great service!",
                "Very professional",
                "Would recommend",
                "Helped me a lot"
            ]
            service.customer_reviews = random.sample(reviews, review_count)
            service.save()
        
        print(f"Created service: {service.name} by {owner.email}")

if __name__ == '__main__':
    create_seed_services()