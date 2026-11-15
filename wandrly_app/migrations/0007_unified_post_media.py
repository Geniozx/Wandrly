import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wandrly_app", "0006_backfill_post_media"),
    ]

    operations = [
        migrations.RenameField(
            model_name="postmedia",
            old_name="image",
            new_name="file",
        ),
        migrations.AlterField(
            model_name="postmedia",
            name="file",
            field=models.FileField(upload_to="posts/"),
        ),
        migrations.AddField(
            model_name="post",
            name="cover_image",
            field=models.ImageField(
                upload_to="posts/covers/",
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="postmedia",
            name="media_type",
            field=models.CharField(
                max_length=10,
                choices=[
                    ("image", "Image"),
                    ("video", "Video"),
                ],
                default="image",
            ),
        ),
        migrations.AddField(
            model_name="postmedia",
            name="thumbnail",
            field=models.ImageField(
                upload_to="posts/thumbnails/",
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="postmedia",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="media_items",
                to="wandrly_app.post",
            ),
        ),
    ]
