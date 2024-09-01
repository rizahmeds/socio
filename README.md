# Socio

Socio is a Django-based social networking application that allows users to connect, send friend requests, and manage their friendships.

# Features

- User registration and authentication
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate limiting on friend requests (max 3 requests per minute)
- User profiles with customizable bio and birth date

# Installation

1. Clone the repository:
```
git clone https://github.com/rizahmeds/socio.git
cd socio
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Apply the database migrations:
```
python manage.py migrate
```
5. Create a superuser (admin) account:
```
python manage.py createsuperuser
```
6. Run the development server:
```
python manage.py runserver
```

The application should now be running at http://127.0.0.1:8000/.

# Usage

## API Endpoints

- /api/register/: Register a new user
- /api/login/: Log in a user
- /api/friends/: List friends
- /api/friend-requests/: List, send, accept, or reject friend requests

