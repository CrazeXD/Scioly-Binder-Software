# Generated by Django 5.0.7 on 2024-08-25 00:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(upload_to=""),
        ),
    ]