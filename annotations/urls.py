from django.urls import path

from .views import (
    AnnotationBatchListCreateView,
    AnnotationBatchDetailView,
    AnnotatedImageListCreateView,
    AnnotatedImageDetailView,
    PolygonListCreateView,
    PolygonDetailView,
)

urlpatterns = [
    path(
        "batches/",
        AnnotationBatchListCreateView.as_view(),
        name="annotation-batches",
    ),
    path(
        "batches/<int:pk>/",
        AnnotationBatchDetailView.as_view(),
        name="annotation-batch-detail",
    ),
    path(
        "images/",
        AnnotatedImageListCreateView.as_view(),
        name="annotation-images",
    ),
    path(
        "images/<int:pk>/",
        AnnotatedImageDetailView.as_view(),
        name="annotation-image-detail",
    ),
    path(
        "images/<int:image_id>/polygons/",
        PolygonListCreateView.as_view(),
        name="image-polygons",
    ),
    path(
        "polygons/<int:pk>/",
        PolygonDetailView.as_view(),
        name="polygon-detail",
    ),
]