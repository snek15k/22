from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    preview = models.ImageField(upload_to='blog_previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
