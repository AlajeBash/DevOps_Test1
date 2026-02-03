from django.db import models

class UploadedImage(models.Model):
    original_image = models.ImageField(upload_to='original/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
