LOOG: Ask a question, ask for suggestions, feedback, or opinions about a topic, a product/brand or a photo and get real time conversational responses from relevant informed souls.

Loog (the name comes from Dialogue) is a human-based search where you search for a query, some keywords or tags. In response, the system connects you to people who have been tagged with those keywords based on the quality and quantity of their dialogues in the past. Not only Dialogue, you or a bot can create a poll to get expert decision making performance. 

Eventually, we will provide a rest api (and JS) so that Loog can be accessed from anywhere on the web. For example, if someone is reading a news article and wants to talk about it, there will be a Loog link next to the URL (or any other content with text or appropriate metadata) that will take the user to Loog. We will use the text/metadata to automatically generate tags and start a conversation! Loog will initiate a dialogue via a tweet, news article, Wikipedia page, a research paper, etc. It also integrates with e-commerce services so that shoppers can instantly have a chat about the product or category they are reviewing.



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

    GOOGLE_CLIENT_ID=place-key-here
    GOOGLE_CLIENT_SECRET=place-key-here
    GOOGLE_APPLICATION_CREDENTIALS=absolute_path_to_credentials.json
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




