from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, NotifyViewSet

router = DefaultRouter()
router.register('contact', ContactViewSet, basename='contact')
router.register('notify', NotifyViewSet, basename='notify')

urlpatterns = [
    path('', include(router.urls)),
]
