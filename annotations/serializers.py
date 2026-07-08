from rest_framework import serializers

from .models import AnnotatedImage, PolygonAnnotation


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class PolygonAnnotationSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(read_only=True)
    points = PointSerializer(many=True)

    class Meta:
        model = PolygonAnnotation
        fields = [
            'id',
            'image',
            'label',
            'points',
            'color',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'image',
            'created_at',
        ]

    def validate_points(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "A polygon must have at least 3 points."
            )

        return value


class AnnotatedImageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField()
    polygons = PolygonAnnotationSerializer(many=True, read_only=True)

    class Meta:
        model = AnnotatedImage
        fields = [
            'id',
            'user',
            'title',
            'image',
            'image_url',
            'width',
            'height',
            'uploaded_at',
            'polygons',
        ]

        read_only_fields = [
            'id',
            'user',
            'image_url',
            'width',
            'height',
            'uploaded_at',
            'polygons',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')

        if obj.image:
            url = obj.image.url

            if request:
                return request.build_absolute_uri(url)

            return url

        return None