from django.core.management.base import BaseCommand
from categories.models import Category
from authors.models import Author
from posts.models import Post
from django.utils import timezone
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = ["Tech", "News", "Gaming", "Music", "Science"]
        for c in categories:
            Category.objects.get_or_create(name=c)

        authors = [
            ("Alice", "alice@mail.com"),
            ("Bob", "bob@mail.com"),
            ("Carlos", "carlos@mail.com"),
        ]
        for name, email in authors:
            Author.objects.get_or_create(display_name=name, email=email)

        categories = list(Category.objects.all())
        authors = list(Author.objects.all())

        for i in range(30):
            Post.objects.create(
                title=f"Post {i}",
                body="Contenido de ejemplo",
                author=random.choice(authors),
                category=random.choice(categories),
                status="published",
                published_at=timezone.now(),
            )

        print("Seed ejecutado ✅")
