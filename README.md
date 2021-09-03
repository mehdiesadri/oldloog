## Tech Stack
- Python
- Django
- HTML, CSS, JS
- MySQL
- Redis
- Celery and celery beat
- SMTP
- Nginx, gunicorn and daphne

## Quick Start
1. Clone repository
2. Change directory to the cloned repository
3. Create a `.env` file in the root directory:
    ```dotenv
    SECRET_KEY=place-secret-key-here
    ALLOWED_HOSTS=localhost,127.0.0.1,web
    DJANGO_SETTINGS_MODULE=loog.settings.production

    DATABASE_NAME=loog_db
    DATABASE_USER=root
    DATABASE_PASSWORD=place-password-here
    DATABASE_HOST=db
    DATABASE_PORT=3306

    REDIS_HOST=redis
    REDIS_PORT=6379

    MYSQL_DATABASE=loog_db
    MYSQL_ROOT_PASSWORD=place-password-here

    EMAIL_PASSWORD=place-password-here

    VAPID_PUBLIC_KEY=place-key-here
    VAPID_PRIVATE_KEY=place-key-here

    GOOGLE_CLIENT_ID=place-key-here
    GOOGLE_CLIENT_SECRET=place-key-here
    ```
4. Run `docker-compose up --build`

## Django Apps

### Main
Static pages like landing page, about, contact us ant etc.
- Home page
- About page

### Accounts
Everything related to user accounts.
- Login
- Logout
- Register
- Profile 
- Invite users

### Chat
Everything related to chat service.
- Chat sessions
- Chat history

### Discovery
Everything related to search and user tags.
- Tags
- User search

### Notifications
Everything related to notification service
- In-app notifications
- System notifications
- Web push notifications
- Email-based notifications

## Code Style for Each App
- `utils.py` for utility functions.
- `selectors.py` for fetch data from database.
- `services.py` for writing data to database.
- `signals.py` for attaching model signals.
- `tasks.py` for defining celery tasks.
- `consumers.py` for web socket consumers.
- `api/` views, serializers and routers for API.
- `tests/` for testing important functionalities.




