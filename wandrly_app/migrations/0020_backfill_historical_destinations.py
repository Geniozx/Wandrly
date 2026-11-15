
from django.db import migrations


HISTORICAL_DESTINATIONS = (
    {
        "name": "Aguas Calientes, Peru",
        "slug": "aguas-calientes-peru",
        "country": "Peru",
        "city": "Aguas Calientes",
        "state": "",
        "location_ids": (1,),
    },
    {
        "name": "Jacksonville, Florida, United States",
        "slug": "jacksonville-florida-united-states",
        "country": "United States",
        "city": "Jacksonville",
        "state": "Florida",
        "location_ids": (2, 3),
    },
    {
        "name": "Ica, Peru",
        "slug": "ica-peru",
        "country": "Peru",
        "city": "Ica",
        "state": "Ica",
        "location_ids": (4,),
    },
    {
        "name": "Rio Grande, Puerto Rico",
        "slug": "rio-grande-puerto-rico",
        "country": "Puerto Rico",
        "city": "Rio Grande",
        "state": "",
        "location_ids": (5, 6),
    },
)


def backfill_destinations(apps, schema_editor):
    Destination = apps.get_model("wandrly_app", "Destination")
    Location = apps.get_model("wandrly_app", "Location")
    db_alias = schema_editor.connection.alias

    for item in HISTORICAL_DESTINATIONS:
        locations = list(
            Location.objects.using(db_alias)
            .filter(pk__in=item["location_ids"])
            .order_by("pk")
        )

        if len(locations) != len(item["location_ids"]):
            raise RuntimeError(
                "Historical location records are missing for "
                f"{item['slug']}"
            )

        for location in locations:
            if location.destination_id is not None:
                raise RuntimeError(
                    f"Location {location.pk} already has a destination"
                )
            
        expected_locations = {
            1: ("Aguas Calientes", "Peru"),
            2: ("Jacksonville, Fl", "United States"),
            3: ("Jacksonville, Fl", "United States"),
            4: ("Ica", "Lima"),
            5: ("Rio Grande", "Puerto Rico"),
            6: ("Rio Grande", "Puerto Rico"),
        }

        for location in locations:
            expected_city, expected_country = expected_locations[
                location.pk
            ]

            if (
                location.city != expected_city
                or location.country != expected_country
            ):
                raise RuntimeError(
                    "Historical location mismatch for "
                    f"Location {location.pk}"
                )

        destination, created = (
            Destination.objects.using(db_alias).get_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "country": item["country"],
                    "state": item["state"],
                    "city": item["city"],
                },
            )
        )

        if not created:
            raise RuntimeError(
                f"Destination slug already exists: {item['slug']}"
            )

        Location.objects.using(db_alias).filter(
            pk__in=item["location_ids"]
        ).update(destination_id=destination.pk)


def reverse_backfill(apps, schema_editor):
    Destination = apps.get_model("wandrly_app", "Destination")
    Location = apps.get_model("wandrly_app", "Location")
    db_alias = schema_editor.connection.alias

    for item in HISTORICAL_DESTINATIONS:
        destination = (
            Destination.objects.using(db_alias)
            .filter(slug=item["slug"])
            .first()
        )

        if destination is None:
            continue

        Location.objects.using(db_alias).filter(
            pk__in=item["location_ids"],
            destination_id=destination.pk,
        ).update(destination_id=None)

        destination.delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            "wandrly_app",
            "0019_destination_location_destination",
        ),
    ]

    operations = [
        migrations.RunPython(
            backfill_destinations,
            reverse_backfill,
        ),
    ]
