from PIL import Image as PILImage

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnnotationBatch, AnnotatedImage, PolygonAnnotation
from .serializers import (
    AnnotationBatchSerializer,
    AnnotatedImageSerializer,
    PolygonAnnotationSerializer,
)


class AnnotationBatchListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        batches = (
            AnnotationBatch.objects.filter(user=request.user)
            .prefetch_related("images__polygons")
            .order_by("-created_at")
        )

        serializer = AnnotationBatchSerializer(
            batches,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        uploaded_files = request.FILES.getlist("images")

        if not uploaded_files:
            return Response(
                {"detail": "No images were uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        batch_title = request.data.get("title", "")

        batch = AnnotationBatch.objects.create(
            user=request.user,
            title=batch_title or f"Image Batch",
        )

        for uploaded_file in uploaded_files:
            width = None
            height = None

            try:
                with PILImage.open(uploaded_file) as img:
                    width, height = img.size

                uploaded_file.seek(0)
            except Exception:
                pass

            AnnotatedImage.objects.create(
                user=request.user,
                batch=batch,
                image=uploaded_file,
                title=uploaded_file.name,
                width=width,
                height=height,
            )

        serializer = AnnotationBatchSerializer(
            batch,
            context={"request": request},
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnnotationBatchDetailView(generics.DestroyAPIView):
    serializer_class = AnnotationBatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnotationBatch.objects.filter(user=self.request.user)


class AnnotatedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnotatedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            AnnotatedImage.objects.filter(user=self.request.user)
            .prefetch_related("polygons")
            .order_by("-uploaded_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnnotatedImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnotatedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnotatedImage.objects.filter(user=self.request.user).prefetch_related(
            "polygons"
        )


class PolygonListCreateView(generics.ListCreateAPIView):
    serializer_class = PolygonAnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        image_id = self.kwargs.get("image_id")

        return PolygonAnnotation.objects.filter(
            image_id=image_id,
            image__user=self.request.user,
        ).order_by("created_at")

    def perform_create(self, serializer):
        image_id = self.kwargs.get("image_id")

        image = AnnotatedImage.objects.get(
            id=image_id,
            user=self.request.user,
        )

        serializer.save(image=image)


class PolygonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PolygonAnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PolygonAnnotation.objects.filter(image__user=self.request.user)