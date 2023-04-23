import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def create_custom_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{slugify(instance.user)}-{uuid.uuid4()}{ext}"
    return os.path.join("posts/", filename)


class Post(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    text = models.TextField()
    image = models.ImageField(null=True, upload_to=create_custom_path)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="likes", on_delete=models.CASCADE
    )
