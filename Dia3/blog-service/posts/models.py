from django.db import models
from slugify import slugify
from authors.models import Author
from categories.models import Category

class Post(models.Model):
    STATUS = (("draft", "Draft"), ("published", "Published"))

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
