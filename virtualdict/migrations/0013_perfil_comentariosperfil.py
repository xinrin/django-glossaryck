# Generated by Django 4.2.5 on 2023-12-14 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("virtualdict", "0012_alter_concepts_exampleimg_comentarios"),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True)),
                (
                    "foto",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComentariosPerfil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("texto", models.TextField()),
                ("fecha_publicacion", models.DateTimeField(auto_now_add=True)),
                (
                    "comentador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comentador",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_perfil",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_perfil",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
