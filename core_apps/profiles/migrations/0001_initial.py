# Generated by Django 4.1.1 on 2022-09-16 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+254722000000",
                        max_length=30,
                        region=None,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "about_me",
                    models.TextField(
                        default="Say something about yourself", verbose_name="about me"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "male"),
                            ("female", "female"),
                            ("other", "other"),
                        ],
                        default="other",
                        max_length=20,
                        verbose_name="gender",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="KE", max_length=2, verbose_name="country"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        default="Nairobi", max_length=50, verbose_name="city"
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(
                        default="profile_default.png",
                        upload_to="",
                        verbose_name="profile photo",
                    ),
                ),
                (
                    "twitter_handle",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="twitter handle",
                    ),
                ),
                (
                    "follows",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="followed_by",
                        to="profiles.profile",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]