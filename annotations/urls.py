from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnnotatedImageViewSet, PolygonAnnotationViewSet


router = DefaultRouter()
router.register('images', AnnotatedImageViewSet, basename='annotation-images')
router.register('polygons', PolygonAnnotationViewSet, basename='annotation-polygons')


urlpatterns = [
    path('', include(router.urls)),
]