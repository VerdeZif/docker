from rest_framework import viewsets, mixins, filters
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer

@method_decorator(cache_page(60), name="retrieve")   # Cache solo detalle
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.filter(status="published").select_related("author", "category")
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "body"]  # ?search=

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostListSerializer
