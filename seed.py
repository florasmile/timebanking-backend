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
            "latitude": 47.62,
            "longitude": -122.34
        },
        {
            "email": "michael.johnson@example.com",
            "first_name": "Michael",
            "last_name": "Johnson",
            "bio": "Financial analyst working in Columbia Center",
            "skills": "Investment Strategies, Excel, Data Visualization",
            "interests": ["wine tasting", "sailing"],
            "time_credits": 5.0,
            "street": "701 5th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.61,
            "longitude": -122.33
        },
        {
            "email": "emily.wong@example.com",
            "first_name": "Emily",
            "last_name": "Wong",
            "bio": "Hotel concierge at The Four Seasons",
            "skills": "Hospitality, Event Planning, Japanese",
            "interests": ["food tours", "theater"],
            "time_credits": 8.0,
            "street": "99 Union St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.60,
            "longitude": -122.32
        },
        {
            "email": "david.kim@example.com",
            "first_name": "David",
            "last_name": "Kim",
            "bio": "Barista at Cherry Street Coffee",
            "skills": "Latte Art, Coffee Roasting, Customer Service",
            "interests": ["live music", "skateboarding"],
            "time_credits": 3.0,
            "street": "103 Cherry St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.63,
            "longitude": -122.35
        },
        {
            "email": "sarah.miller@example.com",
            "first_name": "Sarah",
            "last_name": "Miller",
            "bio": "Public defender at King County Courthouse",
            "skills": "Legal Research, Public Speaking, Spanish",
            "interests": ["social justice", "hiking"],
            "time_credits": 6.0,
            "street": "516 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.59,
            "longitude": -122.31
        },
        {
            "email": "james.rodriguez@example.com",
            "first_name": "James",
            "last_name": "Rodriguez",
            "bio": "Tour guide for Seattle Underground Tour",
            "skills": "Public Speaking, History, Photography",
            "interests": ["urban exploration", "craft beer"],
            "time_credits": 4.0,
            "street": "614 1st Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.64,
            "longitude": -122.36
        },
        {
            "email": "oliver.martinez@example.com",
            "first_name": "Oliver",
            "last_name": "Martinez",
            "bio": "Mixologist at Canon cocktail bar",
            "skills": "Craft Cocktails, Flair Bartending, Spirits Knowledge",
            "interests": ["cocktail competitions", "vinyl records"],
            "time_credits": 6.0,
            "street": "928 12th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98102",
            "latitude": 47.62,
            "longitude": -122.31
        },
        {
            "email": "isabella.nguyen@example.com",
            "first_name": "Isabella",
            "last_name": "Nguyen",
            "bio": "Owner of a Capitol Hill vintage clothing store",
            "skills": "Fashion Styling, Vintage Curating, Small Business",
            "interests": ["thrifting", "drag shows"],
            "time_credits": 4.0,
            "street": "1501 Broadway Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98102",
            "latitude": 47.63,
            "longitude": -122.32
        },
        {
            "email": "ethan.johnson@example.com",
            "first_name": "Ethan",
            "last_name": "Johnson",
            "bio": "Software engineer at Adobe, Wallingford resident",
            "skills": "JavaScript, UI Design, Technical Writing",
            "interests": ["board games", "home brewing"],
            "time_credits": 5.0,
            "street": "1723 N 45th St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98103",
            "latitude": 47.66,
            "longitude": -122.33
        },
        {
            "email": "mia.chen@example.com",
            "first_name": "Mia",
            "last_name": "Chen",
            "bio": "Elementary school teacher at Green Lake",
            "skills": "Curriculum Development, Mandarin, Classroom Management",
            "interests": ["children's literature", "hiking"],
            "time_credits": 7.0,
            "street": "3901 Woodlawn Ave N",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98103",
            "latitude": 47.67,
            "longitude": -122.34
        },
        {
            "email": "lucas.wilson@example.com",
            "first_name": "Lucas",
            "last_name": "Wilson",
            "bio": "Chef at The Walrus and the Carpenter",
            "skills": "Oyster Shucking, French Cuisine, Food Safety",
            "interests": ["fishing", "fermentation"],
            "time_credits": 3.0,
            "street": "1443 N 46th St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98103",
            "latitude": 47.65,
            "longitude": -122.35
        }, 
        {
            "email": "ava.patel@example.com",
            "first_name": "Ava",
            "last_name": "Patel",
            "bio": "UW grad student in marine biology",
            "skills": "Lab Research, Scientific Writing, SCUBA Diving",
            "interests": ["ocean conservation", "yoga"],
            "time_credits": 2.0,
            "street": "4707 17th Ave NE",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98105",
            "latitude": 47.66,
            "longitude": -122.30
        },
        {
            "email": "noah.kim@example.com",
            "first_name": "Noah",
            "last_name": "Kim",
            "bio": "Bookstore manager at University Book Store",
            "skills": "Literary Criticism, Inventory Management, Event Planning",
            "interests": ["poetry slams", "book binding"],
            "time_credits": 5.0,
            "street": "4326 University Way NE",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98105",
            "latitude": 47.67,
            "longitude": -122.31
        },
        {
            "email": "sophia.gonzalez@example.com",
            "first_name": "Sophia",
            "last_name": "Gonzalez",
            "bio": "Barista at Cafe Allegro",
            "skills": "Latte Art, Coffee Roasting, Customer Service",
            "interests": ["live music", "urban sketching"],
            "time_credits": 4.0,
            "street": "4214 University Way NE",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98105",
            "latitude": 47.65,
            "longitude": -122.32
        },
        {
            "email": "william.jackson@example.com",
            "first_name": "William",
            "last_name": "Jackson",
            "bio": "Research scientist at UW Medical Center",
            "skills": "Data Analysis, Python, Medical Research",
            "interests": ["science outreach", "mountain biking"],
            "time_credits": 6.0,
            "street": "4545 15th Ave NE",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98105",
            "latitude": 47.64,
            "longitude": -122.33
        },
        {
            "email": "charlotte.brown@example.com",
            "first_name": "Charlotte",
            "last_name": "Brown",
            "bio": "Librarian at UW Suzzallo Library",
            "skills": "Research Methods, Archival Preservation, Information Systems",
            "interests": ["historical fiction", "tea culture"],
            "time_credits": 4.0,
            "street": "4000 15th Ave NE",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98105",
            "latitude": 47.68,
            "longitude": -122.29
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