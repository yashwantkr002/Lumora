# Lumora

Lumora ek full-stack social media platform hai jo Django ke saath banaya gaya hai. Is project mein user authentication, profiles, posts, reels, likes, comments, search aur responsive UI ka support hai.

## Features

- User registration, login aur logout
- User profile management
- Post creation aur post detail view
- Image/video upload support
- Reels support
- Likes aur comments
- Search functionality
- Password reset aur OTP-based verification
- Responsive frontend design

## Tech Stack

- Python
- Django
- SQLite (current setup) / PostgreSQL support possible
- Tailwind CSS
- JavaScript
- Django Allauth
- Django Cleanup / Session Timeout

## Folder Structure

```text
Lumora/
├── app/
│   ├── migrations/
│   ├── templates/
│   └── views.py
├── static/
├── templates/
├── media/
├── theme/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## Installation

1. Virtual environment activate karen:
   ```bash
   env\\Scripts\\activate
   ```

2. Dependencies install karen:
   ```bash
   pip install -r requirements.txt
   ```

3. Database migrations run karen:
   ```bash
   python manage.py migrate
   ```

4. Development server start karen:
   ```bash
   python manage.py runserver
   ```

## Notes

- Project mein current mein SQLite database use ho rahi hai.
- Static aur media folders images, posts, reels aur frontend assets ke liye use ho rahe hain.
