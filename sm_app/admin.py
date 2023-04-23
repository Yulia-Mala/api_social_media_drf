from django.contrib import admin

from sm_app.models import Post, Like, Comment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
