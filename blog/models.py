from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    publish = models.DateField(default=timezone.now,null=True, blank=True)
    image = models.ImageField(upload_to='ocr_images/',null=True, blank=True)
    summary = models.TextField(default="No summary provided")
    uploaded_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})