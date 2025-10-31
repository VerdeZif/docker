from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "author", "category", "published_at"]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
