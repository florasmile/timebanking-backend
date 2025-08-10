import os
import django
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from accounts.models import User

def create_seed_users():
    demo_users = [
        # Belltown (3 users)
        {
            "email": "alex.johnson@example.com",
            "first_name": "Alex",
            "last_name": "Johnson",
            "bio": "Software engineer and amateur chef",
            "skills": "Python, Cooking, Photography",
            "interests": ["hiking", "coding"],
            "time_credits": 5.0,
            "street": "2321 2nd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98121",
            "latitude": 47.61,
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
            "street": "2719 4th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98121",
            "latitude": 47.62,
            "longitude": -122.35
        },
        {
            "email": "emily.wong@example.com",
            "first_name": "Emily",
            "last_name": "Wong",
            "bio": "Hotel concierge at The Four Seasons",
            "skills": "Hospitality, Event Planning, Japanese",
            "interests": ["food tours", "theater"],
            "time_credits": 8.0,
            "street": "2211 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98121",
            "latitude": 47.60,
            "longitude": -122.33
        },
        
        # Central District (3 users)
        {
            "email": "david.kim@example.com",
            "first_name": "David",
            "last_name": "Kim",
            "bio": "Barista at Cherry Street Coffee",
            "skills": "Latte Art, Coffee Roasting, Customer Service",
            "interests": ["live music", "skateboarding"],
            "time_credits": 3.0,
            "street": "1801 23rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.61,
            "longitude": -122.30
        },
        {
            "email": "sarah.miller@example.com",
            "first_name": "Sarah",
            "last_name": "Miller",
            "bio": "Public defender at King County Courthouse",
            "skills": "Legal Research, Public Speaking, Spanish",
            "interests": ["social justice", "hiking"],
            "time_credits": 6.0,
            "street": "1516 19th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.62,
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
            "street": "1423 21st Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.60,
            "longitude": -122.29
        },
        
        # Queen Anne (3 users)
        {
            "email": "oliver.martinez@example.com",
            "first_name": "Oliver",
            "last_name": "Martinez",
            "bio": "Mixologist at Canon cocktail bar",
            "skills": "Craft Cocktails, Flair Bartending, Spirits Knowledge",
            "interests": ["cocktail competitions", "vinyl records"],
            "time_credits": 6.0,
            "street": "320 W Galer St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98119",
            "latitude": 47.63,
            "longitude": -122.36
        },
        {
            "email": "isabella.nguyen@example.com",
            "first_name": "Isabella",
            "last_name": "Nguyen",
            "bio": "Owner of a vintage clothing store",
            "skills": "Fashion Styling, Vintage Curating, Small Business",
            "interests": ["thrifting", "drag shows"],
            "time_credits": 4.0,
            "street": "500 1st Ave N",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98109",
            "latitude": 47.62,
            "longitude": -122.37
        },
        {
            "email": "ethan.johnson@example.com",
            "first_name": "Ethan",
            "last_name": "Johnson",
            "bio": "Software engineer at Adobe",
            "skills": "JavaScript, UI Design, Technical Writing",
            "interests": ["board games", "home brewing"],
            "time_credits": 5.0,
            "street": "223 8th Ave W",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98119",
            "latitude": 47.64,
            "longitude": -122.35
        },
        
        # First Hill (3 users)
        {
            "email": "mia.chen@example.com",
            "first_name": "Mia",
            "last_name": "Chen",
            "bio": "Elementary school teacher",
            "skills": "Curriculum Development, Mandarin, Classroom Management",
            "interests": ["children's literature", "hiking"],
            "time_credits": 7.0,
            "street": "1016 Boylston Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98104",
            "latitude": 47.60,
            "longitude": -122.32
        },
        {
            "email": "lucas.wilson@example.com",
            "first_name": "Lucas",
            "last_name": "Wilson",
            "bio": "Chef at local restaurant",
            "skills": "Oyster Shucking, French Cuisine, Food Safety",
            "interests": ["fishing", "fermentation"],
            "time_credits": 3.0,
            "street": "1215 Seneca St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "latitude": 47.61,
            "longitude": -122.33
        },
        {
            "email": "ava.patel@example.com",
            "first_name": "Ava",
            "last_name": "Patel",
            "bio": "Medical student at UW",
            "skills": "Lab Research, Scientific Writing, SCUBA Diving",
            "interests": ["ocean conservation", "yoga"],
            "time_credits": 2.0,
            "street": "815 9th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98104",
            "latitude": 47.59,
            "longitude": -122.31
        },
        
        # Capitol Hill (3 users)
        {
            "email": "noah.kim@example.com",
            "first_name": "Noah",
            "last_name": "Kim",
            "bio": "Bookstore manager",
            "skills": "Literary Criticism, Inventory Management, Event Planning",
            "interests": ["poetry slams", "book binding"],
            "time_credits": 5.0,
            "street": "1501 10th Ave E",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98102",
            "latitude": 47.62,
            "longitude": -122.32
        },
        {
            "email": "sophia.gonzalez@example.com",
            "first_name": "Sophia",
            "last_name": "Gonzalez",
            "bio": "Barista at local cafe",
            "skills": "Latte Art, Coffee Roasting, Customer Service",
            "interests": ["live music", "urban sketching"],
            "time_credits": 4.0,
            "street": "1212 11th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.63,
            "longitude": -122.31
        },
        {
            "email": "william.jackson@example.com",
            "first_name": "William",
            "last_name": "Jackson",
            "bio": "Research scientist",
            "skills": "Data Analysis, Python, Medical Research",
            "interests": ["science outreach", "mountain biking"],
            "time_credits": 6.0,
            "street": "1313 12th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.61,
            "longitude": -122.30
        },
        
        # South Lake Union (3 users)
        {
            "email": "charlotte.brown@example.com",
            "first_name": "Charlotte",
            "last_name": "Brown",
            "bio": "UX Designer at Amazon",
            "skills": "UI/UX Design, User Research, Prototyping",
            "interests": ["historical fiction", "tea culture"],
            "time_credits": 4.0,
            "street": "400 Fairview Ave N",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98109",
            "latitude": 47.62,
            "longitude": -122.34
        },
        {
            "email": "liam.smith@example.com",
            "first_name": "Liam",
            "last_name": "Smith",
            "bio": "Biotech researcher",
            "skills": "Molecular Biology, Data Analysis, Lab Techniques",
            "interests": ["rock climbing", "science fiction"],
            "time_credits": 5.0,
            "street": "500 Mercer St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98109",
            "latitude": 47.63,
            "longitude": -122.33
        },
        {
            "email": "amelia.jones@example.com",
            "first_name": "Amelia",
            "last_name": "Jones",
            "bio": "Software developer at Tableau",
            "skills": "Data Visualization, SQL, Business Intelligence",
            "interests": ["data journalism", "yoga"],
            "time_credits": 6.0,
            "street": "600 Westlake Ave N",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98109",
            "latitude": 47.61,
            "longitude": -122.35
        },
        
        # Cherry Hill (2 users)
        {
            "email": "benjamin.taylor@example.com",
            "first_name": "Benjamin",
            "last_name": "Taylor",
            "bio": "High school teacher",
            "skills": "History, Curriculum Development, Debate Coaching",
            "interests": ["historical reenactment", "gardening"],
            "time_credits": 4.0,
            "street": "2701 E Cherry St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98122",
            "latitude": 47.60,
            "longitude": -122.30
        },
        {
            "email": "harper.white@example.com",
            "first_name": "Harper",
            "last_name": "White",
            "bio": "Graphic designer",
            "skills": "Adobe Creative Suite, Branding, Illustration",
            "interests": ["printmaking", "indie music"],
            "time_credits": 3.0,
            "street": "2600 E Jefferson St",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98112",
            "latitude": 47.59,
            "longitude": -122.29
        }, 
        # Bellevue (5 users)
        {
            "email": "ryan.carter@example.com",
            "first_name": "Ryan",
            "last_name": "Carter",
            "bio": "Cloud architect at Microsoft",
            "skills": "Azure, DevOps, System Design",
            "interests": ["tech meetups", "mountain biking"],
            "time_credits": 6.0,
            "street": "11020 NE 10th St",
            "city": "Bellevue",
            "state": "WA",
            "zip_code": "98004",
            "latitude": 47.62,
            "longitude": -122.20
        },
        {
            "email": "natalie.lee@example.com",
            "first_name": "Natalie",
            "last_name": "Lee",
            "bio": "UX designer at T-Mobile",
            "skills": "Figma, User Research, Prototyping",
            "interests": ["art galleries", "indie films"],
            "time_credits": 5.0,
            "street": "500 108th Ave NE",
            "city": "Bellevue",
            "state": "WA",
            "zip_code": "98004",
            "latitude": 47.61,
            "longitude": -122.18
        },
        {
            "email": "daniel.park@example.com",
            "first_name": "Daniel",
            "last_name": "Park",
            "bio": "Financial advisor at Edward Jones",
            "skills": "Retirement Planning, Investment Strategies",
            "interests": ["golf", "wine collecting"],
            "time_credits": 7.0,
            "street": "1400 112th Ave SE",
            "city": "Bellevue",
            "state": "WA",
            "zip_code": "98005",
            "latitude": 47.59,
            "longitude": -122.15
        },
        {
            "email": "olivia.chen@example.com",
            "first_name": "Olivia",
            "last_name": "Chen",
            "bio": "Pastry chef at local bakery",
            "skills": "French Patisserie, Cake Decorating",
            "interests": ["food blogging", "yoga"],
            "time_credits": 4.0,
            "street": "15600 NE 8th St",
            "city": "Bellevue",
            "state": "WA",
            "zip_code": "98008",
            "latitude": 47.63,
            "longitude": -122.12
        },
        {
            "email": "ethan.wilson@example.com",
            "first_name": "Ethan",
            "last_name": "Wilson",
            "bio": "Real estate agent specializing in Eastside",
            "skills": "Market Analysis, Property Valuation",
            "interests": ["hiking", "photography"],
            "time_credits": 5.0,
            "street": "330 112th Ave NE",
            "city": "Bellevue",
            "state": "WA",
            "zip_code": "98004",
            "latitude": 47.58,
            "longitude": -122.22
        },
        
        # Redmond (5 users)
        {
            "email": "sophia.nguyen@example.com",
            "first_name": "Sophia",
            "last_name": "Nguyen",
            "bio": "Game developer at Nintendo",
            "skills": "Unity, C#, 3D Modeling",
            "interests": ["esports", "anime"],
            "time_credits": 6.0,
            "street": "7501 164th Ave NE",
            "city": "Redmond",
            "state": "WA",
            "zip_code": "98052",
            "latitude": 47.67,
            "longitude": -122.10
        },
        {
            "email": "liam.jackson@example.com",
            "first_name": "Liam",
            "last_name": "Jackson",
            "bio": "Robotics engineer at Microsoft Research",
            "skills": "ROS, Python, Machine Learning",
            "interests": ["DIY electronics", "trail running"],
            "time_credits": 5.0,
            "street": "8601 161st Ave NE",
            "city": "Redmond",
            "state": "WA",
            "zip_code": "98052",
            "latitude": 47.66,
            "longitude": -122.08
        },
        {
            "email": "ava.kim@example.com",
            "first_name": "Ava",
            "last_name": "Kim",
            "bio": "Biotech researcher at Philips Healthcare",
            "skills": "Medical Imaging, Data Analysis",
            "interests": ["science outreach", "pottery"],
            "time_credits": 4.0,
            "street": "17625 NE 65th St",
            "city": "Redmond",
            "state": "WA",
            "zip_code": "98052",
            "latitude": 47.69,
            "longitude": -122.05
        },
        {
            "email": "noah.garcia@example.com",
            "first_name": "Noah",
            "last_name": "Garcia",
            "bio": "Cybersecurity specialist at Facebook",
            "skills": "Ethical Hacking, Network Security",
            "interests": ["lock picking", "chess"],
            "time_credits": 7.0,
            "street": "15900 NE 31st St",
            "city": "Redmond",
            "state": "WA",
            "zip_code": "98052",
            "latitude": 47.65,
            "longitude": -122.12
        },
        {
            "email": "isabella.patel@example.com",
            "first_name": "Isabella",
            "last_name": "Patel",
            "bio": "Product manager at SpaceX",
            "skills": "Agile Development, Market Research",
            "interests": ["astronomy", "rock climbing"],
            "time_credits": 5.0,
            "street": "2200 148th Ave NE",
            "city": "Redmond",
            "state": "WA",
            "zip_code": "98052",
            "latitude": 47.70,
            "longitude": -122.15
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