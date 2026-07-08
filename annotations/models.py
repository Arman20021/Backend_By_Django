from django.conf import settings
from django.db import models
from PIL import Image as PILImage
from django.contrib.auth.models import User



class AnnotationBatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Batch {self.id}"

class AnnotatedImage(models.Model):
    batch = models.ForeignKey(
        AnnotationBatch,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='annotations/')
    title = models.CharField(max_length=255, blank=True)

    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and (self.width is None or self.height is None):
            try:
                img = PILImage.open(self.image.path)
                width, height = img.size

                self.width = width
                self.height = height

                super().save(update_fields=['width', 'height'])
            except Exception:
                pass

    def __str__(self):
        return self.title or f"Image {self.id}"


class PolygonAnnotation(models.Model):
    image = models.ForeignKey(
        AnnotatedImage,
        on_delete=models.CASCADE,
        related_name='polygons'
    )

    label = models.CharField(max_length=100, default='Tumor')
    points = models.JSONField()
    color = models.CharField(max_length=20, default='#8b5cf6')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.label} on image {self.image_id}"