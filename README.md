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



### Phase 3 — Saved Posts & Bookmarks ✅

Established the database foundation for Roamly's Saved Posts feature.

#### SavedPost Model

- Stores bookmarks linking users to saved posts.
- Supports both travel posts and travel journal entries through the unified Post model.
- Records when each bookmark was created.
- Orders saved posts by most recently saved.
- Provides reverse relationships:
  - `user.saved_posts`
  - `post.saved_by`
- Prevents duplicate bookmarks using the `unique_saved_post` database constraint.
- Uses Django cascade deletion for bookmarks when their associated user or post is deleted.

#### Database Migration

Migration `0009_savedpost.py`:

- Creates the `SavedPost` table.
- Adds foreign keys to User and Post.
- Adds database indexes and the unique bookmark constraint.
- Does not modify existing users, profiles, posts, or media.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Applied migration `0009` successfully.
- Verified valid bookmark creation.
- Verified duplicate bookmarks are rejected.
- Verified user and post relationships.
- Confirmed temporary test records were rolled back.
- Django system checks passed.
- No additional migrations detected.

#### Future API Implementation

The Django REST API will support:

- Saving and unsaving posts.
- Retrieving a user's saved posts.
- Checking whether a post is saved by the current user.
- Privacy-aware access to saved content.
- Pagination and ordering for saved posts.

Saving a post will not override its visibility or the author's profile privacy settings.

Cascade deletion behavior is configured in the model and will receive dedicated testing during API development.


### Phase 3 — Notifications Foundation ✅

Established the database foundation for Roamly's in-app notification system.

#### Notification Model

Supports five notification types:

- `new_follower` — A user gains a new follower.
- `follow_request` — A private profile receives a follow request.
- `follow_accepted` — A follow request is accepted.
- `post_like` — Someone likes a post.
- `post_comment` — Someone comments on a post.

Each notification includes:

- `recipient` — User receiving the notification.
- `actor` — User who triggered the event.
- `notification_type` — Type of notification.
- `post` — Optional related post.
- `follow_request` — Optional related follow request.
- `is_read` — Read/unread status, defaulting to false.
- `created_at` — Creation timestamp.

#### Database Constraints and Performance

- Prevents users from generating notifications to themselves.
- Includes the `notification_inbox_idx` composite index for recipient, read status, and creation time.
- Supports ordering by newest notifications first.
- Uses Django foreign-key relationships for associated users, posts, and follow requests.

#### Database Migration

Migration `0010_notification.py`:

- Creates the Notification table.
- Adds foreign keys and supporting indexes.
- Adds the self-notification prevention constraint.
- Preserves existing users, profiles, posts, and media.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Applied migration `0010` successfully.
- Verified notification creation with unread status.
- Verified marking notifications as read and unread.
- Verified self-notification attempts are rejected.
- Verified unread notification inbox queries.
- Confirmed all temporary test records were rolled back.
- Django system checks passed.
- All migrations through `0010` applied.
- No additional model changes detected.

#### Future API Implementation

The Django REST API will provide:

- Automatic notification creation for supported social events.
- Authenticated notification inbox endpoints.
- Mark-as-read and mark-as-unread operations.
- Unread notification counts.
- Pagination and ordering.
- Authorization and privacy-aware notification details.
- Event-specific validation and duplicate-event handling.

Notification delivery and automatic event generation are not yet implemented.



### Phase 3B — User Blocking Foundation ✅

Established the database foundation for user blocking and unblocking in Roamly 2.0.

#### UserBlock Model

Introduced the `UserBlock` model with:

- `blocker` — User initiating the block.
- `blocked` — User receiving the block.
- `created_at` — Timestamp recording when the block was created.

#### Database Relationships and Constraints

- `blocked_users` — Access accounts blocked by a user.
- `blocked_by_users` — Access accounts that have blocked a user.
- `unique_user_block` — Prevents duplicate blocking relationships.
- `prevent_self_block` — Prevents users from blocking themselves.
- Foreign-key indexes support efficient relationship queries.

#### Migration

Migration `0011_userblock.py`:

- Creates the `UserBlock` database table.
- Adds foreign keys and integrity constraints.
- Preserves all existing user, profile, post, and social data.
- Applies to the isolated `roamly_dev` database.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0011`.
- Verified valid blocking relationships.
- Verified forward and reverse relationship queries.
- Confirmed duplicate blocks are rejected.
- Confirmed self-blocking is rejected.
- Rolled back all temporary test records.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Future API Implementation

The Django REST API will implement:

- Block and unblock actions.
- Removal of existing follow relationships when blocking.
- Cancellation of pending follow requests.
- Restrictions on following, commenting, mentioning, and other interactions.
- Privacy-aware profile, post, and media access.
- A blocked accounts management interface.

Blocking behavior and authorization are not yet implemented in the API.


### Phase 3B — Threaded Comments Foundation ✅

Extended Roamly 2.0's existing comment system to support
nested conversations while preserving historical Wandrly data.

#### Comment Model Enhancements

Updated the existing `Comment` model with:

- `parent` — Nullable self-referencing foreign key allowing
  replies to comments and other replies.
- `replies` — Reverse relationship for accessing direct replies.
- `updated_at` — Automatically tracks comment modifications.
- `user.comments` — Reverse relationship for accessing a user's comments.
- Chronological ordering by `created_at` and `id`.

#### Database Integrity

Migration `0012` introduces:

- `comment_thread_idx` — Composite index on
  `post`, `parent`, and `created_at`.
- `prevent_self_comment_reply` — Database constraint
  preventing direct self-referencing comments.
- Nullable parent relationships to preserve existing comments.

#### Historical Data Preservation

A custom `RunPython` migration initializes historical
`updated_at` values using the original `created_at` timestamp.

Verified that the original Wandrly comment retains:

- Comment ID: 1
- Post ID: 4
- Original creation timestamp
- Matching historical update timestamp
- No parent comment

No existing comment content or ownership was modified.

#### Verification

- Migration `0012` applied successfully.
- Original historical comment preserved.
- Top-level comment creation verified.
- Replies to comments verified.
- Replies to replies verified.
- Reverse reply relationships verified.
- Automatic update timestamps verified.
- Direct self-referencing replies rejected.
- Temporary test records rolled back.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

The upcoming API and React implementation will provide:

- Threaded comment conversations.
- Replies to comments and replies.
- Visually limited reply indentation.
- Expandable and collapsible reply threads.
- Comment editing and deletion.
- Comment and reply likes.
- @username mentions and notifications.
- Relative timestamps with exact dates available.
- Pagination and comment sorting.
- Cross-post reply validation.
- Circular reply-chain prevention.
- Privacy and blocked-user interaction enforcement.

These behaviors are planned and are not yet implemented
in the API or frontend.


### Phase 3B — Comment Likes Foundation ✅

Established the database foundation for liking comments and
nested replies in Roamly 2.0.

#### CommentLike Model

Introduced the `CommentLike` model with:

- `user` — User who liked the comment or reply.
- `comment` — Comment or nested reply receiving the like.
- `created_at` — Timestamp recording when the like occurred.

#### Relationships and Constraints

- `comment.likes` — Access likes associated with a comment.
- `user.comment_likes` — Access comments liked by a user.
- `unique_comment_like` — Prevents duplicate likes from
  the same user on the same comment.
- Foreign-key indexes support efficient relationship queries.
- Chronological ordering by newest likes first.

Because replies use the existing `Comment` model, likes on
top-level comments and nested replies share one database table.

#### Migration

Migration `0013_commentlike.py`:

- Creates the `wandrly_app_commentlike` table.
- Adds foreign keys to the existing User and Comment models.
- Enforces unique user/comment like relationships.
- Preserves existing comments, replies, posts, and users.
- Applies to the isolated `roamly_dev` PostgreSQL database.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0013`.
- Verified creation of comment likes.
- Verified multiple users can like the same comment.
- Verified reverse relationship queries.
- Confirmed duplicate likes are rejected.
- Verified likes on nested replies.
- Confirmed comment and reply like counts.
- Rolled back all temporary test records.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

The upcoming Django REST API and React frontend will support:

- Like and unlike actions on comments and replies.
- Displaying comment and reply like counts.
- Showing whether the authenticated user liked a comment.
- Privacy-aware comment interactions.
- Blocked-user interaction restrictions.
- Comment-like notifications.
- Efficient pagination and query optimization.

These features are planned and are not yet implemented
in the API or frontend.
