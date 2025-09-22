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
