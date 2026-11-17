
from django.db.models import Q

from wandrly_app.models import Follow, UserBlock


def users_are_blocked(viewer, target_user):
    if not viewer.is_authenticated:
        return False

    return UserBlock.objects.filter(
        Q(blocker=viewer, blocked=target_user)
        | Q(blocker=target_user, blocked=viewer)
    ).exists()


def is_approved_follower(viewer, target_user):
    if not viewer.is_authenticated:
        return False

    return Follow.objects.filter(
        follower=viewer,
        following=target_user,
    ).exists()


def can_view_profile_content(viewer, profile):
    if viewer.is_authenticated and viewer.pk == profile.user_id:
        return True

    if users_are_blocked(viewer, profile.user):
        return False

    if not profile.is_private:
        return True

    return is_approved_follower(viewer, profile.user)
