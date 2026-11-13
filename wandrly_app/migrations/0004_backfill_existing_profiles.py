from django.conf import settings
from django.db import migrations


def backfill_existing_profiles(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Profile = apps.get_model("wandrly_app", "Profile")

    db_alias = schema_editor.connection.alias

    existing_profile_user_ids = Profile.objects.using(
        db_alias
    ).values_list("user_id", flat=True)

    missing_users = User.objects.using(db_alias).exclude(
        pk__in=existing_profile_user_ids
    )

    Profile.objects.using(db_alias).bulk_create(
        [
            Profile(
                user_id=user.pk,
                display_name=(
                    f"{user.first_name} {user.last_name}".strip()
                    or user.username
                ),
                is_private=False,
            )
            for user in missing_users
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        (
            "wandrly_app",
            "0003_post_post_type_post_updated_at_post_visibility_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            backfill_existing_profiles,
            migrations.RunPython.noop,
        ),
    ]
