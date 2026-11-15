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



---

## Roamly 2.0 — Phase 3: Database Schema Modernization

### Milestone 1 — Profile and Post Foundations ✅

Development database: `roamly_dev`

#### Migration 0003 — Profile and Post Schema

Extended the existing Django models without replacing their original records or relationships.

Profile enhancements:
- `display_name` — public-facing profile name
- `avatar` — optional profile image
- `is_private` — account privacy setting, defaulting to public

Post enhancements:
- `post_type` — travel post or travel journal
- `visibility` — public or private
- `updated_at` — automatic modification timestamp

Historical posts retain their original `created_at` values. The migration backfills `updated_at` from `created_at`.

The original Post.media field remains intact pending the future multi-image migration.

#### Migration 0004 — Existing Profile Backfill

Created missing Profile records for existing users using a historical-model data migration.

- Existing users preserved: 2
- Profiles after migration: 2
- Default account privacy: public
- Existing authentication records preserved

#### Post-Migration Integrity Verification

All checks passed:

- Users: 2
- Profiles: 2
- Posts: 3
- Comments: 1
- Locations: 6
- Post media files: 3 of 3 available
- Existing posts default to travel/public
- Historical post timestamps preserved
- No unexpected model changes detected

Both migrations were successfully applied to `roamly_dev`.

The original `wandrly` database remains outside the migration target.

### Next Milestone

Introduce the PostMedia model to support multiple ordered images per post while preserving existing media references.



### Phase 3 — Unified Post Media Foundation ✅

**Status:** Completed

Implemented the database foundation for multiple images,
multiple videos, mixed-media posts, and optional custom
post cover images.

#### Unified PostMedia Model

Added the `PostMedia` model with:

- Foreign key to `Post` (`related_name="media_items"`)
- Media type classification: image or video
- File storage through Django's `FileField`
- Zero-based media ordering using `position`
- Optional video thumbnail image
- Optional accessibility description (`alt_text`)
- Automatic creation timestamp
- Unique constraint on `(post, position)`
- Default ordering by `position`, then `id`

#### Custom Post Covers

Added `Post.cover_image`:

- Optional image field
- Stored under `posts/covers/`
- Independent of the post's media attachments
- Intended for profile grids, feeds, and Explore cards

Automatic cover fallback behavior will be implemented
during the API and frontend development phases.

#### Database Migrations

- `0005_postmedia`
  - Created the original multi-image PostMedia table.

- `0006_backfill_post_media`
  - Backfilled existing image references into PostMedia.
  - Preserved original image paths.
  - Avoided duplicate media records.

- `0007_unified_post_media`
  - Renamed `PostMedia.image` to `PostMedia.file`.
  - Changed ImageField to FileField.
  - Added media type classification.
  - Added optional video thumbnail field.
  - Added optional Post cover image field.
  - Updated the reverse relationship to `media_items`.

#### Historical Data Verification

Validated against the isolated `roamly_dev` database:

- Existing posts: 3
- Unified media records: 3
- All historical media classified as images
- All media positions preserved at zero
- All original and new file paths match
- All referenced physical files exist
- All legacy `Post.media` references preserved
- All seven application migrations applied
- No outstanding model changes

**Result:** All unified media integrity checks passed.

#### Backward Compatibility

The original `Post.media` field remains available
because existing Django forms and templates depend on it.

#### Future Implementation

The database now supports storing image and video
attachment references.

The following functionality is planned but not yet
implemented:

- Multiple file uploads per post
- Mixed-media carousel interfaces
- Video file validation and size limits
- Video processing and thumbnail generation
- Custom cover upload and automatic cover fallback
- Secure media access respecting post privacy
- Video playback and responsive media presentation


### Phase 3 — Social Relationships & Follow Requests ✅

Established the database foundation for Roamly's social following system.

#### Follow Model

- Stores approved follower relationships between users.
- Supports follower and following queries through related names.
- Records when each relationship was created.
- Prevents duplicate follower relationships.
- Prevents users from following themselves.
- Automatically removes relationships when associated users are deleted.

#### FollowRequest Model

- Stores requests to follow private profiles.
- Supports four statuses:
  - `pending`
  - `accepted`
  - `declined`
  - `canceled`
- Tracks creation and modification timestamps.
- Prevents duplicate request pairs.
- Prevents users from requesting to follow themselves.
- Supports incoming and outgoing follow-request queries.

#### Database Migration

Migration `0008_follow_followrequest.py`:

- Creates the `Follow` table.
- Creates the `FollowRequest` table.
- Adds foreign keys, indexes, and database constraints.
- Preserves existing users, profiles, posts, and media.

#### Verification

- Django system checks passed.
- Migration `0008` applied successfully to `roamly_dev`.
- Valid follow relationships and requests were created successfully.
- Duplicate follow relationships were rejected.
- Self-follow attempts were rejected.
- Duplicate follow requests were rejected.
- Self-follow requests were rejected.
- Test records were rolled back successfully.
- Django detected no additional model changes.

#### Future API Implementation

The Django REST API will handle:

- Immediate following of public profiles.
- Follow requests for private profiles.
- Accepting, declining, and canceling follow requests.
- Unfollowing users.
- Re-requesting access after declined or canceled requests.
- Transactional approval of follow requests.
- Privacy-aware access to profiles, posts, and media.
