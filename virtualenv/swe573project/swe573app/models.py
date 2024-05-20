from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Community(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # new field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    templates = models.ManyToManyField("CommunityTemplate", blank=True)
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
