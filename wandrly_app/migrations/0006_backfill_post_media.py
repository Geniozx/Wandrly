from django.db import migrations


def backfill_post_media(apps, schema_editor):
    Post = apps.get_model("wandrly_app", "Post")
    PostMedia = apps.get_model("wandrly_app", "PostMedia")

    db_alias = schema_editor.connection.alias

    posts = Post.objects.using(db_alias).exclude(
        media=""
    ).exclude(
        media__isnull=True
    )

    for post in posts.iterator():
        PostMedia.objects.using(db_alias).get_or_create(
            post_id=post.pk,
            position=0,
            defaults={
                "image": post.media.name,
                "alt_text": "",
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("wandrly_app", "0005_postmedia"),
    ]

    operations = [
        migrations.RunPython(
            backfill_post_media,
            migrations.RunPython.noop,
        ),
    ]
