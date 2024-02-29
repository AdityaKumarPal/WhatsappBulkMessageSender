# MyWebApp/models.py
from django.db import models

class UserData(models.Model):
    name = models.CharField(max_length=255)
    numbers_file = models.FileField(upload_to='uploads/csv/')
    image = models.ImageField(upload_to='uploads/images/')
    video = models.FileField(upload_to='uploads/videos/')
    document = models.FileField(upload_to='uploads/documents/')
    message = models.TextField()

    def __str__(self):
        return self.name
