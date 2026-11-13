# Wandrly
![alt text](wandrly_app/static/images/wandrly_pin_softcoral_teal.svg)

**Wandrly** is a Django-based web application for sharing posts with location data. Users can create posts with images, captions, and locations, and view posts on an interactive map.

---

## Technologies Used

- **Python 3.11**
- **Django 5.2**
- **GeoDjango** (Django’s geographic web framework)
- **PostgreSQL + PostGIS** (for geospatial database support)
- **Leaflet.js** (for interactive maps)  
  [Leaflet.js Setup Guide](https://medium.com/@harumhelmy/getting-started-with-leaflet-js-7f96a3c7ea5a)
- **HTML5, CSS3, JavaScript**
- **Django Templates**

---

## Features

- User authentication (signup, login, logout)
- Profile management
- Create, edit, and delete posts
- Upload images for posts
- Comment on posts
- Like posts
- Interactive map to display post locations

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Geniozx/Wandrly
    cd Wandrly
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup PostgreSQL with PostGIS:**
    - Create a database and user in PostgreSQL.
    - Ensure PostGIS extension is enabled.
    - Configure `DATABASES` in `settings.py`.

    [GeoDjango Installation Guide](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/)

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the app:**
    Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Styling & UI

- The site uses a **soft coral and teal color scheme**.
- Navigation bar across the top for ease of access.
- Post cards are styled to be **compact, elegant, and visually clean**.
- ChatGPT was used to assist in CSS design decisions.

---

## License

This project is for personal and educational purposes. No license assigned.

---

## Acknowledgements

- [Leaflet.js](https://leafletjs.com) for interactive mapping.
- [GeoDjango](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/) for geospatial support.
- ChatGPT for styling and guidance.

---

## Roamly 2.0 — Development Environment

Roamly 2.0 is the modernization of the original Wandrly travel application.

Development takes place on the `develop/roamly-2.0` branch. The original application and database are preserved during the migration.

### Backend Technology

- Python 3.12
- Django 5.2
- PostgreSQL 17.6
- PostGIS 3.6
- Python virtual environment (`.venv`)
- Environment-based Django configuration

The React frontend and Django REST Framework API will be introduced in subsequent development phases.

### Local Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file containing:

```dotenv
SECRET_KEY=<your-local-django-secret-key>
DB_NAME=roamly_dev
DB_USER=wandrly_user
DB_PASSWORD=<your-local-postgresql-password>
DB_HOST=localhost
DB_PORT=5432
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Do not commit `.env` or database credentials.

### Database Isolation

The original PostgreSQL database is named `wandrly`.

Roamly 2.0 development uses a separate restored database named `roamly_dev`.

The development database contains the original application records and migration history.

Local Django settings enforce the expected database name to reduce the risk of accidentally modifying the original database.

Before running migrations, confirm the active database:

```bash
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])"
```

Expected:

```text
roamly_dev
```

### Verification

Run Django's system checks:

```bash
python manage.py check
```

Inspect migration history:

```bash
python manage.py showmigrations
```

Check dependency compatibility:

```bash
python -m pip check
```

### Development Safety

- Keep the original `wandrly` database unchanged.
- Apply future migrations only to `roamly_dev`.
- Preserve existing user, post, comment, and location records.
- Review schema migrations before applying them.
- Keep credentials, virtual environments, and generated files out of Git.
- Preserve the original application's tracked media during migration.

### Phase 2 — Environment Preparation

- [x] Original source and media backed up
- [x] Original PostgreSQL database backed up
- [x] Isolated `roamly_dev` database restored
- [x] PostgreSQL and PostGIS verified
- [x] Development Git branch created
- [x] Original uncommitted changes preserved in Git stash
- [x] Python virtual environment created
- [x] Project `.gitignore` configured
- [x] Django settings updated for environment variables
- [x] Django 5.2 dependencies installed
- [x] Database connection and restored records verified
- [x] Reproducible backend requirements recorded

