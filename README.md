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

| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `POST`   | `/api/signup/`                           | Signup a user.                           |
| `POST`   | `/api/login/`                            | Login a user.                            |
| `GET`    | `/api/users/?search={email/name}?page=2` | Search other users by email and name.    |
| `POST`   | `/api/friends/`                          | Send friend request.                     |
| `PATCH`  | `/api/friends/{id}/accept/`              | Accept friend request.                   |
| `PATCH`  | `/api/friends/{id}/reject/`              | Reject friend request.                   |
| `GET`    | `/api/friends/?status=A`                 | List accepted friend requests.           |
| `GET`    | `/api/friends/?status=P`                 | List pending friend requests.            |
| `GET`    | `/api/friends/?status=R`                 | List rejected friend requests.           |




