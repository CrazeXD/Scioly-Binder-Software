from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from SciBind.settings import MEDIA_ROOT

import os
import random

# Create your models here.


class User(AbstractUser):
    chosen_events = models.ManyToManyField("EventModel", related_name="owners")
    profile_picture = models.ImageField()


def get_random_profile_picture():
    template_dir = os.path.join("lib", "images", "profile_pictures")
    if templates := [
        f for f in os.listdir(template_dir) if f.endswith((".png", ".jpg", ".jpeg"))
    ]:
        return os.path.join(
            "lib", "images", "profile_pictures", random.choice(templates)
        )


@receiver(post_save, sender=User)
def set_random_profile_picture(sender, instance, created, **kwargs):
    if created:
        instance.profile_picture = get_random_profile_picture()
        instance.save()


class EventModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # materialtype can either be 'binder', 'cheat sheet', or 'none'\
    materialchoices = [
        ("Binder", "Binder"),
        ("Cheatsheet", "Cheat Sheet"),
        ("none", "None"),
    ]
    materialtype = models.CharField(max_length=100, choices=materialchoices)
    divchoices = ("A", "B", "C")
    divchoices = [(x, x) for x in divchoices]
    division = models.CharField(max_length=1, choices=divchoices)
    display_image = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    # Check if there are objects of this instance
    def has_objects(self):
        return self.bindermodel_set.exists()


class BinderModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    shared_with = models.ManyToManyField(
        User, related_name="shared_binders", blank=True
    )
    materialtype = models.CharField(
        max_length=100, choices=EventModel.materialchoices, blank=True
    )
    content = models.JSONField(blank=True, null=True)
    old = models.BooleanField(default=False)
    online_users = models.ManyToManyField(
        User, related_name="online_binders", blank=True
    )

    def save(self, *args, **kwargs):
        if self.event:
            self.materialtype = self.event.materialtype
            self.division = self.event.division
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name} Binder - {self.owner.username}"
