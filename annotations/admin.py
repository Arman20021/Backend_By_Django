from django.contrib import admin

from .models import AnnotatedImage, PolygonAnnotation


class PolygonInline(admin.TabularInline):
    model = PolygonAnnotation
    extra = 0


@admin.register(AnnotatedImage)
class AnnotatedImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'width',
        'height',
        'uploaded_at',
    ]

    list_filter = [
        'uploaded_at',
    ]

    search_fields = [
        'title',
        'user__username',
        'user__email',
    ]

    inlines = [PolygonInline]


@admin.register(PolygonAnnotation)
class PolygonAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'image',
        'label',
        'color',
        'created_at',
    ]

    list_filter = [
        'label',
        'created_at',
    ]

    search_fields = [
        'label',
        'image__title',
    ]