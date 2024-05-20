from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
import json
from django.urls import reverse
from django.db.models import JSONField


class Community(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="following", blank=True)
    moderators = models.ManyToManyField(User, related_name="moderating", blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            default_template = Template.objects.create(
                name="Default Template",
                fields=json.dumps(
                    [
                        {"name": "Header", "type": "str"},
                        {"name": "Content", "type": "str"},
                    ]
                ),
                community=self,
            )
            self.templates.add(default_template)


class Template(models.Model):
    name = models.CharField(max_length=100)
    fields = JSONField()
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="templates"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("template_detail", args=[str(self.id)])


class CommunityTemplate(models.Model):
    name = models.CharField(max_length=200)
    fields = models.JSONField()  # Stores a list of field definitions
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="community_templates",
        default=None,
        null=True,
    )

    def clean(self):
        try:
            json.loads(self.fields)
        except ValueError:
            raise ValidationError("Fields must be valid JSON")


class Post(models.Model):
    title = models.CharField(max_length=200, default="DefaultTitle")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="posts", null=True
    )  # Use a unique related_name for the Post model

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    template = models.ForeignKey(CommunityTemplate, on_delete=models.CASCADE, default=1)
    data = models.JSONField(
        default=dict
    )  # Stores the actual post data according to the template


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
