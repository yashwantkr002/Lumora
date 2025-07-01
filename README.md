# Mvideos - A Django Video Sharing Platform

This is a Django-based web application for sharing videos, similar to a social media platform for videos. Users can create accounts, upload videos (reels), manage their profiles, and interact with content.

## Project Structure

- `Mvideos/`: Main Django project configuration, including settings, URLs, and WSGI/ASGI configurations.
- `app/`: The core Django application containing models, views, templates, and static files for user management, posts, and other functionalities.
- `media/`: Stores user-uploaded content like post images, profile pictures, and video reels.
- `static/`: Contains static assets such as CSS, JavaScript, and images.
- `templates/`: Houses HTML templates for rendering web pages.
- `env/`: A Python virtual environment for managing project dependencies.
- `db.sqlite3`: The default SQLite database file.
- `manage.py`: Django's command-line utility for administrative tasks.

## Features (Inferred)

- User authentication (registration, login, password reset)
- User profiles with profile pictures
- Video (reels) uploading and display
- Image posting
- Admin interface for managing content and users

## Setup Instructions

To set up and run this project locally, follow these steps:

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository_url>
    cd Mvideos
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv env
    .\env\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

## Technologies Used

-   Django (Python Web Framework)
-   SQLite (Default Database)
-   HTML, CSS, JavaScript

## Contributing

(Add instructions for contributing if this is an open-source project)

## License

(Specify the project's license)