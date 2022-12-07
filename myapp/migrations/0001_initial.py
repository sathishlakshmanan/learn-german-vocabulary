# Generated by Django 4.1.3 on 2022-11-21 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Articles",
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
                ("article_name", models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserCreation",
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
                ("user_name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="CreateVocabulary",
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
                ("word_de", models.CharField(max_length=30)),
                ("word_en", models.CharField(max_length=30)),
                ("sentence", models.CharField(max_length=100)),
                ("creation_time", models.DateTimeField(auto_now_add=True)),
                ("article", models.ManyToManyField(to="myapp.articles")),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.usercreation",
                    ),
                ),
            ],
        ),
    ]
