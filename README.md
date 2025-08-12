# TimeBank (Back-End)

Backend for our group project built with **Django** and **PostgreSQL**.

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

## 🤝 Team

- Dehui Hu
- Malik Elmessiry
- Mikaela Baluyot
- Natasha Gaye
