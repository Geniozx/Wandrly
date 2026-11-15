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


### Phase 3B — Expanded Notifications Foundation ✅

Extended Roamly 2.0's notification database foundation to
support threaded comment interactions and user mentions.

#### Notification Types

The Notification model now supports eight event types:

Existing notification types:
- `new_follower` — New follower.
- `follow_request` — Follow request received.
- `follow_accepted` — Follow request accepted.
- `post_like` — Post liked.
- `post_comment` — New post comment.

New notification types:
- `comment_reply` — Reply to a comment or nested reply.
- `comment_like` — Like on a comment or nested reply.
- `user_mention` — User mentioned in a comment or reply.

#### Comment Relationship

Added a nullable `comment` foreign key to the Notification
model with the reverse relationship `comment.notifications`.

This enables notifications to reference the relevant comment
or reply while preserving compatibility with existing
notification types that do not require comment references.

#### Migration

Migration `0014_notification_comment_and_more.py`:

- Adds the nullable `comment_id` column.
- Creates the foreign-key constraint to Comment.
- Adds an index on `comment_id`.
- Extends the notification type choices from five to eight.
- Preserves existing notification relationships and constraints.
- Does not modify historical notification records.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0014`.
- Verified all eight notification types.
- Verified creation of notifications with comment and post references.
- Confirmed notifications default to unread.
- Verified reverse comment notification relationships.
- Confirmed self-notifications are rejected.
- Rolled back all temporary test records.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

The upcoming API and React frontend will implement:

- Automatic notification creation for supported events.
- Notifications for replies, comment likes, and mentions.
- Notification recipient validation.
- Privacy and blocked-user enforcement.
- Notification preferences.
- Mark-as-read and unread notification management.
- Navigation to referenced posts, comments, and replies.
- Relative timestamps with exact dates available.
- Pagination and efficient notification queries.

The database foundation is complete. Automatic notification
generation and user-facing behavior are not yet implemented.


### Phase 3B — Notification Preferences Foundation ✅

Established the database foundation for user-controlled
notification preferences in Roamly 2.0.

#### NotificationPreference Model

Introduced the `NotificationPreference` model with a
one-to-one relationship to Django's existing User model.

Each user can configure eight notification categories:

- `new_followers` — New follower notifications.
- `follow_requests` — Incoming follow requests.
- `follow_accepted` — Accepted follow requests.
- `post_likes` — Likes on posts.
- `post_comments` — Comments on posts.
- `comment_replies` — Replies to comments.
- `comment_likes` — Likes on comments and replies.
- `user_mentions` — Mentions in comments and replies.

All eight settings default to `True`.

The model also includes:

- `created_at` — Preference record creation timestamp.
- `updated_at` — Last modification timestamp.
- `notification_preferences` — Reverse one-to-one user relationship.

#### Database Integrity

The one-to-one relationship enforces a unique preference
record per user.

Each user can configure notification categories independently
without affecting other users.

Existing user records remain unchanged. Preference records
can be created when first needed by the application.

#### Migration

Migration `0015_notificationpreference.py`:

- Creates the `wandrly_app_notificationpreference` table.
- Adds eight boolean notification preference columns.
- Adds creation and modification timestamps.
- Creates a unique `user_id` relationship.
- References the existing `auth_user` table.
- Preserves all existing users and notifications.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0015`.
- Verified independent preference records for two users.
- Confirmed all eight preferences default to enabled.
- Verified individual preferences can be disabled.
- Confirmed changes to one user do not affect another.
- Verified reverse one-to-one relationships.
- Confirmed duplicate preference records are rejected.
- Verified original user records remain intact.
- Rolled back all temporary test changes.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

The upcoming Django REST API and React frontend will support:

- Retrieving the authenticated user's preferences.
- Creating missing preference records when needed.
- Updating individual notification categories.
- Enforcing preferences during notification generation.
- Managing preferences through account settings.
- Applying privacy and blocked-user restrictions.

These behaviors are planned and are not yet implemented
in the API or frontend.


### Phase 3B — Post Drafts & Publishing State Foundation ✅

Established the database foundation for saving drafts and
publishing travel posts and journals in Roamly 2.0.

#### Publication Status

Extended the existing Post model with two publication states:

- `draft` — An unfinished post that has not been published.
- `published` — A post that has been published.

The `publication_status` field defaults to `published` to
preserve compatibility with historical posts.

Publication status remains separate from post visibility.

The existing `visibility` field continues to support:

- `public`
- `private`

This allows drafts to retain their intended visibility
before publication.

#### Publication Timestamp

Added a nullable `published_at` field.

- Drafts can exist without a publication timestamp.
- Published posts can record their first publication time.
- Editing a published post should preserve its original
  publication timestamp.
- The publishing API will manage publication transitions.

#### Historical Data Preservation

Migration `0016` includes a controlled data backfill.

Existing published posts receive their original `created_at`
timestamp as their `published_at` value.

The backfill uses Django's historical model registry and
the migration's database connection.

Historical post IDs `1`, `4`, and `6` remain unchanged.

Existing captions, visibility settings, media relationships,
and creation timestamps are preserved.

#### Migration

Migration
`0016_post_publication_status_post_published_at.py`:

- Adds `publication_status` to the Post model.
- Adds nullable `published_at`.
- Defaults historical posts to `published`.
- Backfills publication timestamps from `created_at`.
- Preserves existing post and media relationships.
- Uses a reversible schema migration with a no-op
  reverse operation for the data backfill.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0016`.
- Verified historical post IDs `1`, `4`, and `6`.
- Confirmed all historical posts remain published.
- Verified original publication timestamps.
- Confirmed historical visibility remains public.
- Successfully created a temporary draft.
- Verified drafts can have a null publication timestamp.
- Tested a draft-to-published transition.
- Confirmed editing preserved the publication timestamp.
- Rolled back all temporary test records.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

The upcoming Django REST API and React frontend will support:

- Creating and saving unfinished drafts.
- Editing and deleting owned drafts.
- Publishing drafts as travel posts or journals.
- Preserving the first publication timestamp.
- Separating publication status from visibility.
- Restricting draft access to the owner.
- Excluding drafts from public feeds, search, and maps.
- Supporting draft management in the user interface.
- Warning users about unsaved changes.

The database foundation is complete. Draft access controls,
publishing workflows, and frontend functionality are not
yet implemented.


### Phase 3B — Content Reporting Foundation ✅

Established the database foundation for reporting inappropriate
accounts, posts, comments, and threaded replies in Roamly 2.0.

#### ContentReport Model

Introduced `ContentReport` to support reporting three target types:

- User accounts
- Posts
- Comments, including threaded replies

Each report records:

- Reporter
- Exactly one reported target
- Report reason
- Optional additional details
- Moderation status
- Creation timestamp
- Last modification timestamp

Reports are ordered by newest creation timestamp, followed by ID.

#### Report Reasons

The following standardized reasons are supported:

- `spam` — Spam
- `harassment` — Harassment or Bullying
- `hate_abuse` — Hate or Abusive Content
- `inappropriate` — Inappropriate Content
- `impersonation` — Impersonation
- `other` — Other

#### Moderation Statuses

Reports support four moderation statuses:

- `pending` — Awaiting review
- `under_review` — Being reviewed
- `resolved` — Reviewed and resolved
- `dismissed` — Reviewed and dismissed

New reports default to `pending`.

#### Database Integrity

Migration `0017_contentreport.py` introduces the
`report_exactly_one_target` PostgreSQL CHECK constraint.

This constraint requires exactly one of the following:

- `reported_user`
- `reported_post`
- `reported_comment`

The database rejects reports with no target or multiple targets.

Foreign key relationships connect reports to existing users,
posts, and comments.

No historical users, posts, comments, or media were modified.

#### Verification

- Confirmed the target database was `roamly_dev`.
- Successfully applied migration `0017`.
- Verified reports against users, posts, and comments.
- Confirmed new reports default to `pending`.
- Verified reports without a target are rejected.
- Verified reports with multiple targets are rejected.
- Tested moderation status transitions.
- Rolled back all temporary report records.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Moderation Behavior

The upcoming API and moderation workflows will implement:

- Authenticated report submission.
- Prevention of self-reporting.
- Reporter privacy and restricted report visibility.
- Moderator-only review and status changes.
- Report submission rate limiting.
- Duplicate and abusive report handling.
- Reporting controls for posts, profiles, and comments.
- Appropriate handling of private and blocked content.
- Moderation history and audit requirements.

#### Production Considerations

The current model uses cascading deletion for reported
users, posts, and comments.

Deleting a reported target can therefore delete its
associated reports.

Before production, the moderation architecture must address
evidence retention, deletion behavior, and audit history.

The reporting database foundation is complete. Report APIs,
moderator permissions, and moderation interfaces are not
yet implemented.


### Phase 3B — Post Comment Controls Foundation ✅

Established the database foundation for author-controlled
comment settings on Roamly 2.0 posts and travel journals.

#### Post Comment Settings

Extended the existing `Post` model with:

- `comments_enabled` — BooleanField, default `True`.

The setting allows post authors to enable or disable new
comments and replies without deleting existing discussions.

All historical posts default to having comments enabled,
preserving existing application behavior.

#### Intended Comment Behavior

When comments are enabled:

- Authorized users can submit comments.
- Authorized users can reply to existing comments.
- Existing discussions remain accessible according to
  post visibility and account privacy rules.

When comments are disabled:

- New comments must be rejected.
- New replies must be rejected.
- Existing comments and replies remain preserved.
- Existing comment likes remain preserved.
- Authors can re-enable comments later.

The database stores the setting. API-level enforcement
will be implemented in Phase 4.

#### Migration

Migration `0018_post_comments_enabled.py`:

- Depends on `0017_contentreport`.
- Adds `comments_enabled` to the existing Post model.
- Uses `BooleanField(default=True)`.
- Preserves historical posts and their comment settings.
- Does not modify Comment, CommentLike, or PostMedia.

#### Historical Data Preservation

Verified that historical posts `1`, `4`, and `6` retain
their original IDs and have comments enabled.

Confirmed the historical comment associated with post `4`
remains intact.

Existing comment records, reply relationships, and comment
likes were compared before and after temporarily changing
a post's comment setting.

No historical discussion records were modified.

#### Verification

- Confirmed the development database was `roamly_dev`.
- Successfully applied migration `0018`.
- Verified historical posts have comments enabled.
- Confirmed the historical comment on post `4`.
- Tested disabling comments.
- Verified existing comments and likes were preserved.
- Tested re-enabling comments.
- Rolled back all temporary changes.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned API and Frontend Behavior

Phase 4 and subsequent frontend development will implement:

- Author-only permission to change comment settings.
- Rejection of new comments when comments are disabled.
- Rejection of new replies when comments are disabled.
- Preservation of existing discussion threads.
- Privacy-aware access to existing comments.
- Appropriate comment and reply controls in the UI.
- Clear messaging when comments are disabled.

The database foundation is complete. Comment submission
restrictions and author-facing controls are not yet implemented.


### Phase 3B — Destination Tagging Foundation ✅

Established the database foundation for canonical travel
destinations, geographic discovery, and destination pages.

#### Destination Model

Introduced `Destination` with:

- `name` — Human-readable destination name.
- `slug` — Unique, stable URL identifier.
- `country` — Country or territory name.
- `state` — Optional state or region.
- `city` — Optional city.
- `continent` — Optional continent.
- `created_at` — Creation timestamp.
- `updated_at` — Modification timestamp.

Destinations represent shared geographic identities rather
than individual map coordinates.

#### Location-to-Destination Relationship

Extended the existing `Location` model with:

- `destination` — Nullable ForeignKey to Destination.
- `on_delete=SET_NULL`.
- `related_name="locations"`.

Multiple Location records can reference one Destination.

The existing Post.location relationship remains unchanged:

Post → Location → Destination

This preserves compatibility with historical posts and
their existing Leaflet map coordinates.

#### Migration

Migration `0019_destination_location_destination.py`:

- Depends on `0018_post_comments_enabled`.
- Creates the Destination database table.
- Adds a nullable destination foreign key to Location.
- Creates the necessary database indexes.
- Does not modify historical location coordinates.
- Does not modify historical post associations.
- Does not automatically create destination records.

#### Historical Data Preservation

Verified all six historical Location records remain intact.

Verified historical Post.location associations:

- Post 1 → Location 1
- Post 4 → Location 4
- Post 6 → Location 6

All existing Location.destination values remain NULL
until a controlled destination backfill is performed.

#### Integrity Testing

- Confirmed the active database was roamly_dev.
- Successfully applied migration 0019.
- Verified all six historical locations.
- Verified all three historical post associations.
- Confirmed the Destination table was initially empty.
- Created a temporary Rio Grande destination.
- Associated Locations 5 and 6 with that destination.
- Verified both locations shared the destination.
- Verified the existing Post.location relationship.
- Rolled back all temporary destination changes.
- Confirmed historical data remained unchanged.
- Django system checks passed.
- No pending migrations or model changes detected.

#### Planned Destination Backfill

A separate, controlled data migration will:

- Create canonical destination records.
- Associate existing locations with destinations.
- Preserve historical location IDs and coordinates.
- Preserve historical post relationships.
- Handle duplicate city records safely.
- Review inconsistent historical geographic metadata.

The historical Ica/Lima classification and potentially
inconsistent Jacksonville coordinates require explicit
review rather than silent modification.

#### Planned API and Frontend Features

Future phases will implement:

- Destination-specific pages and URLs.
- Destination-based post discovery.
- Geographic search and filtering.
- Destination-aware map exploration.
- Privacy-aware destination feeds.
- Destination tagging during post creation and editing.

The database foundation is complete. Historical destination
backfilling and destination-facing APIs are not yet implemented.


### Phase 3B — Historical Destination Backfill ✅

Populated the canonical Destination model using existing
Wandrly location records without modifying historical
geographic coordinates or post associations.

#### Migration

Migration `0020_backfill_historical_destinations.py`:

- Depends on `0019_destination_location_destination`.
- Uses Django RunPython with historical model access.
- Creates four canonical destination records.
- Associates six historical locations with those destinations.
- Validates expected historical location IDs and metadata.
- Rejects unexpected existing destination assignments.
- Rejects conflicting destination slugs.
- Includes a reverse migration for controlled rollback.

#### Canonical Destination Mapping

- Aguas Calientes, Peru: Location 1.
- Jacksonville, Florida, United States: Locations 2 and 3.
- Ica, Peru: Location 4.
- Rio Grande, Puerto Rico: Locations 5 and 6.

#### Historical Data Preservation

The backfill does not modify:

- Original Location IDs.
- Original latitude or longitude values.
- Original city or country values.
- Existing Post.location foreign keys.
- Historical posts and their associated content.

Location 4 retains its historical country value of Lima,
while its canonical destination identifies Ica, Peru.

The potentially inconsistent coordinates for Location 2
remain unchanged pending separate geographic validation.

#### Verification

- Confirmed the active database was roamly_dev.
- Successfully applied migration 0020.
- Verified four canonical destinations.
- Verified six destination-to-location associations.
- Confirmed all historical posts retained their locations.
- Verified historical geographic metadata was preserved.
- Verified the destination grouping matches the intended mapping.
- Confirmed Django system checks passed.
- Confirmed no additional model migrations were required.

#### Future Work

- Implement destination serializers and API endpoints.
- Add destination-specific pages.
- Support destination-based search and discovery.
- Enforce post and profile privacy in destination feeds.
- Review geographic metadata inconsistencies.
- Define destination creation and slug collision handling.

Historical destination backfilling is complete.


## Phase 4 — REST API Foundation

### API routing

Roamly 2.0 introduces Django REST Framework with versioned API routes under `/api/v1/`.

The existing Django application routes remain available during the frontend modernization.

**Initial endpoint**

| Method | Endpoint | Authentication |
|---|---|---|
| GET | `/api/v1/health/` | Public |

The health endpoint returns the API's service name, version, and operational status.

### Authentication and permissions

The REST API uses Django session authentication.

Default API permissions require authenticated users. Endpoints intended for public access must explicitly override this default.

CSRF protection is required for authenticated unsafe requests. Authentication endpoints will receive additional CSRF protections during their implementation.

### Automated testing

Three initial API tests verify:

1. The health endpoint returns HTTP 200 and the expected JSON response.
2. Anonymous users can access the health endpoint.
3. Default API permissions reject anonymous access.

The test suite runs against an isolated PostgreSQL test database.

### Historical migration compatibility

Migration `0020_backfill_historical_destinations` supports fresh installations without historical Wandrly locations.

Existing historical data remains subject to validation before destination associations are created.

The original Wandrly database is preserved separately from the Roamly 2.0 development database.