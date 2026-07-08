from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AnnotatedImage, PolygonAnnotation
from .serializers import AnnotatedImageSerializer, PolygonAnnotationSerializer


class AnnotatedImageViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotatedImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return (
            AnnotatedImage.objects
            .filter(user=self.request.user)
            .prefetch_related('polygons')
            .order_by('-uploaded_at')
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        methods=['GET'],
        responses=PolygonAnnotationSerializer(many=True),
    )
    @extend_schema(
        methods=['POST'],
        request=PolygonAnnotationSerializer,
        responses={201: PolygonAnnotationSerializer},
    )
    @action(detail=True, methods=['get', 'post'], url_path='polygons')
    def polygons(self, request, pk=None):
        image = self.get_object()

        if request.method == 'GET':
            polygons = image.polygons.all()
            serializer = PolygonAnnotationSerializer(polygons, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = PolygonAnnotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PolygonAnnotationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PolygonAnnotationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return PolygonAnnotation.objects.filter(
            image__user=self.request.user
        )