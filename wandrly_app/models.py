from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
    )
    is_private = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.user.username



class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_relationship",
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("following")),
                name="prevent_self_follow",
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class FollowRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        CANCELED = "canceled", "Canceled"

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_follow_requests",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "recipient"],
                name="unique_follow_request_pair",
            ),
            models.CheckConstraint(
                condition=~models.Q(requester=models.F("recipient")),
                name="prevent_self_follow_request",
            ),
        ]

    def __str__(self):
        return (
            f"{self.requester.username} -> "
            f"{self.recipient.username}: {self.status}"
        )



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Location(models.Model):
    continent = models.CharField(max_length=50)
    continent_code = models.CharField(max_length=5)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        parts = []
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        if self.continent:
            parts.append(f"({self.continent})")
        return ", ".join(parts) if parts else "Unknown location"



class Post(models.Model):
    class PostType(models.TextChoices):
        TRAVEL = "travel", "Travel Post"
        JOURNAL = "journal", "Travel Journal"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    media = models.ImageField(
        upload_to="posts/",
    )
    cover_image = models.ImageField(
        upload_to="posts/covers/",
        blank=True,
    )
    caption = models.TextField(
        blank=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True,
    )
    post_type = models.CharField(
        max_length=20,
        choices=PostType.choices,
        default=PostType.TRAVEL,
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username}: {self.caption[:2200]}"

    def get_absolute_url(self):
        return reverse(
            "post-detail",
            kwargs={"post_id": self.id},
        )


class PostMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media_items",
    )
    media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )
    file = models.FileField(
        upload_to="posts/",
    )
    thumbnail = models.ImageField(
        upload_to="posts/thumbnails/",
        blank=True,
    )
    position = models.PositiveIntegerField(
        default=0,
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["post", "position"],
                name="unique_post_media_position",
            ),
        ]

    def __str__(self):
        return f"Post {self.post_id} - {self.media_type} {self.position + 1}"


class SavedPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_posts",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="saved_by",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_saved_post",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} saved post {self.post_id}"


class Notification(models.Model):
    class Type(models.TextChoices):
        NEW_FOLLOWER = "new_follower", "New Follower"
        FOLLOW_REQUEST = "follow_request", "Follow Request"
        FOLLOW_ACCEPTED = "follow_accepted", "Follow Request Accepted"
        POST_LIKE = "post_like", "Post Like"
        POST_COMMENT = "post_comment", "Post Comment"

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="triggered_notifications",
    )
    notification_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    follow_request = models.ForeignKey(
        FollowRequest,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(
                fields=["recipient", "is_read", "-created_at"],
                name="notification_inbox_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(recipient=models.F("actor")),
                name="prevent_self_notification",
            ),
        ]

    def __str__(self):
        return (
            f"{self.actor.username} -> "
            f"{self.recipient.username}: {self.notification_type}"
        )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:500]}"