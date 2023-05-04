from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=127)),
                ("author", models.CharField(max_length=127)),
                ("description", models.TextField(blank=True, null=True)),
                ("publish_date", models.CharField(max_length=10)),
                ("number_pages", models.IntegerField()),
                ("language", models.CharField(max_length=20)),
                ("isbn", models.CharField(max_length=13)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="categories.category",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
