# TimeBank (Back-End)

Backend for our group project built with **Django** and **PostgreSQL**.

### 🤝 Team

* Dehui Hu
* Malik Elmessiry
* Mikaela Baluyot
* Natasha Gaye

---

## 🌐 Overview

The TimeBank API powers a service marketplace where users can exchange time-based services with one another.

It supports features such as:

- User sign-up and login with authentication
- Viewing and editing profiles
- Creating and booking services
- Browsing services through an interactive map

---

## 🛠 Tech Stack

- **Python** + **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Cloudinary** for media upload
- **Render** for deployment

<details>
<summary>📦 Dependencies</summary>

```
asgiref==3.9.1
attrs==25.3.0
certifi==2025.7.14
charset-normalizer==3.4.2
cloudinary==1.44.1
dj-database-url==3.0.1
Django==5.2.4
django-cloudinary-storage==0.3.0
django-cors-headers==4.7.0
django-extensions==4.1
djangorestframework==3.16.0
dotenv==0.9.9
drf-spectacular==0.28.0
drf-spectacular-sidecar==2025.7.1
geographiclib==2.0
geopy==2.4.1
gunicorn==23.0.0
idna==3.10
inflection==0.5.1
jsonschema==4.25.0
jsonschema-specifications==2025.4.1
packaging==25.0
psycopg2-binary==2.9.10
python-dotenv==1.1.1
pytz==2025.2
PyYAML==6.0.2
referencing==0.36.2
requests==2.32.4
rpds-py==0.26.0
six==1.17.0
sqlparse==0.5.3
uritemplate==4.2.0
urllib3==2.5.0
whitenoise==6.9.0
```
</details>

---


## 🌍 Deployment

The backend is deployed via **Render** and accessible at:

- 🔗 [Deployed TimeBank Backend](https://timebanking-backend.onrender.com)
- 🔗 [Deployed TimeBank Frontend](https://timebanking-frontend.onrender.com/)

You can explore all available endpoints and test them in-browser using Swagger docs:

- 🔗 [Swagger API Docs](https://timebanking-backend.onrender.com/api/docs/)


---

## 📌 Related Repos

- [TimeBank (Front-End) Repo](https://github.com/malikelmessiry/timebanking-frontend)

---

## 🚀 Getting Started

1. **Clone the repo**:

```bash
git clone https://github.com/florasmile/timebanking-backend.git
cd timebanking-backend
```

2. **Setup and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create PostgreSQL database**:
```bash
psql postgres
# In psql prompt:
CREATE DATABASE timebanking_development;
\q
```

5. **Create and configure your database connection in .env**:
```bash
Copy .env.sample to .env and update as needed
```

6. **Run migrations**:
```bash
python manage.py migrate
```

7. **Start the development server**:
```bash
python manage.py runserver
```

8. **Run tests** (if applicable):
```bash
python manage.py test <app_name>
```

---

### Thank You! 🤝
