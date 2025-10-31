from django.db import models

class Author(models.Model):
    display_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
