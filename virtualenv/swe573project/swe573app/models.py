from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)


class Community(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # new field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(
        "CommunityTemplate", on_delete=models.SET_NULL, null=True
    )
    followers = models.ManyToManyField(User, related_name="following", blank=True)
    moderators = models.ManyToManyField(User, related_name="moderating", blank=True)
    is_active = models.BooleanField(default=True)  # Add this line

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.moderators.add(self.created_by)


class CommunityTemplate(models.Model):
    name = models.CharField(max_length=200)
    fields = models.JSONField()  # This will store a list of field definitions


class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.JSONField()  # This will store the field values
